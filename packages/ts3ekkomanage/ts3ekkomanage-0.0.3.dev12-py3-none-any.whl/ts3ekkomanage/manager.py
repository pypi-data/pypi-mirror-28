import docker
import docker.types
import asyncio
import logging

from ts3ekkoutil.envconsts import EkkoPropertyNames as epn
from ts3ekkoutil.helpers import help_docker_name

from sqlalchemy_seed import load_fixtures, load_fixture_files
from sqlalchemy.exc import IntegrityError

try:
    from ts3ekkomanage.webhooks import EkkoReverseClientContact
    from ts3ekkomanage.envprop import EkkoClientProperties
    from ts3ekkomanage.model import Identity, startup
except ImportError:
    from .webhooks import EkkoReverseClientContact
    from .model import Identity, startup


class EkkoNoIdentityAvailable(Exception):
    def __str__(self):
        return "There is no unused identity avilable."


class TS3EkkoManage:
    def __init__(self, args, loop=None, seed_data=True, spawn_first_client=True):
        self.args = args
        self.loop = loop or asyncio.get_event_loop()
        self.reverse_client_contact = EkkoReverseClientContact(self)
        self.docker_conn = docker.from_env()
        self.dbsession = startup(args[epn.DB_USERNAME], args[epn.DB_PASSWORD], args[epn.DB_HOST], args[epn.DB_DBNAME])

        self.clients = []

        if seed_data:
            self.seed_fixtures()

        if spawn_first_client:
            self.spawn()

    @staticmethod
    def docker_ekko_client_prefix(args):
        return help_docker_name(args[epn.TS3_USERNAME])

    def spawn(self, channel_id=0, channel_password=None, spawn_invoke_event=None):
        # get list of clients
        # check if a client is already in this channel
        # if not, then create new docker container from image and params

        logging.info(f'current existing clients: {self.clients}')

        try:
            new_identity = self.find_unused_identity()

            new_client = self.args.copy()
            new_client[epn.EKKO_NODE_ID] = self.find_unused_node_id()
            new_client[epn.TS3_CHANNEL_ID] = channel_id
            # dont remove the prefix, otherwise containers wont get cleared up on manager restart
            new_client[epn.TS3_USERNAME] = f'{self.docker_ekko_client_prefix(new_client)} ' \
                                           f'{new_client[epn.EKKO_NODE_ID]}'
            new_client[epn.TS3_UNIQUE_ID] = new_identity.unique_ts3_id
            new_client[epn.TS3_IDENTITY] = new_identity.private_identity
            new_client[epn.TS3_CHANNEL_PASSWORD] = channel_password

            media_mount = docker.types.Mount(new_client[epn.EKKO_MEDIA_DIRECTORY],
                                             new_client[epn.EKKO_MEDIA_DIRECTORY_SOURCE], read_only=True,
                                             type='bind')

            self.docker_conn.containers.run(image=self.args[epn.DOCKER_EKKO_CLIENT_IMAGE_NAME], detach=True,
                                            name=help_docker_name(new_client[epn.TS3_USERNAME]),
                                            environment=new_client,
                                            auto_remove=not self.args[epn.DOCKER_DISABLE_AUTOREMOVE],
                                            network=self.args[epn.DOCKER_NETWORK_NAME],
                                            links=[new_client[epn.DOCKER_NETWORK_DBLINK].split(':', maxsplit=1)],
                                            mounts=[media_mount])

            self.clients.append(new_client)
            logging.info(f'spawned new client instance: {new_client[epn.TS3_USERNAME]} // '
                         f'{new_client[epn.EKKO_NODE_ID]}')
        except EkkoNoIdentityAvailable as e:
            # TODO: add response to invoker
            logging.warning(e)
            if spawn_invoke_event is not None:
                pass
            print(e)

    def despawn(self, ekko_node_id):
        # get the client who is in the channel
        # kill it
        for client in self.clients:
            logging.debug(f'probing client for despawn: {client[epn.TS3_USERNAME]}')
            if str(ekko_node_id) == str(client[epn.EKKO_NODE_ID]):
                try:
                    logging.debug(f'despawning container: {help_docker_name(client[epn.TS3_USERNAME])}')
                    self.docker_conn.containers.get(help_docker_name(client[epn.TS3_USERNAME])).stop()
                    self.clients.remove(client)
                except Exception as e:
                    logging.critical(e)

    def find_unused_identity(self):
        all_identities = self.dbsession.query(Identity)
        used_identities = [client[epn.TS3_IDENTITY] for client in self.clients]
        unused_identities = [ident for ident in all_identities if ident.private_identity not in used_identities]
        if unused_identities:
            return unused_identities[0]
        else:
            raise EkkoNoIdentityAvailable()

    def find_unused_node_id(self):
        node_id_list = sorted([client[epn.EKKO_NODE_ID] for client in self.clients])
        if node_id_list:
            return node_id_list[-1] + 1
        else:
            return 1

    def seed_fixtures(self):
        try:
            fixtures = load_fixture_files(self.args[epn.EKKO_FIXTURES_PATH], ['identities.yaml'])
            load_fixtures(self.dbsession, fixtures)
        except IntegrityError:
            logging.info('Identity-fixtures already initialised')
            
        try:
            fixtures = load_fixture_files(self.args[epn.EKKO_FIXTURES_PATH], ['permission.yaml'])
            load_fixtures(self.dbsession, fixtures)
        except IntegrityError:
            logging.info('Permission-fixtures already initialised')

        try:
            fixtures = load_fixture_files(self.args[epn.EKKO_FIXTURES_PATH], ['permission_doc.yaml'])
            load_fixtures(self.dbsession, fixtures)
        except IntegrityError:
            logging.info('Permission_doc-fixtures already initialised')


    async def periodic_update(self, delay=10):
        while True:
            await asyncio.sleep(delay)

    def start(self):
        self.reverse_client_contact.start()
        self.loop.run_until_complete(
            asyncio.wait([
                self.periodic_update(),
            ])
        )
