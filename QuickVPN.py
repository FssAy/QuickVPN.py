import requests
import subprocess
import base64
import io
import os
import uuid
import time
import ctypes
import asyncio
import threading
try:
    from . import Exceptions as Exc
except:
    import Exceptions as Exc


class Connection:
    def __init__(self, country, loop=None):
        self.country = country
        self.loop = loop
        if self.loop is None:
            self.loop = asyncio.new_event_loop()

        self.server = None
        self.server_data = None
        self.path_con_file = None
        self.process = None
        self.thread = None
        self._as_thread = False

    @staticmethod
    def _check_admin():
        try:
            if not ctypes.windll.shell32.IsUserAnAdmin():
                raise Exc.NotAnAdmin()
        except:
            raise Exc.NotAnAdmin()

    def _check_country(self):
        country_len = len(self.country)
        if country_len == 2:
            # short name
            name_index = 6
        elif country_len > 2:
            # long name
            name_index = 5
        else:
            raise Exc.InvalidCountryName(self.country)
        return name_index

    def _get_server(self):
        try:
            # Find all available servers
            vpn_data = requests.get('http://www.vpngate.net/api/iphone/').text.replace('\r', '')
            servers = [line.split(',') for line in vpn_data.split('\n')]
            labels = servers[1]
            labels[0] = labels[0][1:]
            servers = [s for s in servers[2:] if len(s) > 1]
        except:
            raise Exc.NoAvailableServers()

        # Find all servers with desired country name
        name_index = self._check_country()
        desired = [s for s in servers if self.country.lower() in s[name_index].lower()]
        found_amount = len(desired)
        if found_amount == 0:
            raise Exc.NoServersInCountry(self.country)

        # Find all supported servers and pick the best one
        supported = [s for s in desired if len(s[-1]) > 0]
        if len(supported) == 0:
            raise Exc.NoAvailableServers()
        self.server = sorted(supported, key=lambda s: float(s[2].replace(',', '.')), reverse=True)[0]

        pairs = zip(labels, self.server)
        pairs = list(pairs)[:-1]
        self.server_data = {
            'HostName': f'{pairs[0][1]}',
            'IP': f'{pairs[1][1]}',
            'Score': f'{pairs[2][1]}',
            'Ping': f'{pairs[3][1]}',
            'Speed': f'{pairs[4][1]} MBps',
            'Country': pairs[5][1]
        }

    def _create_con_file(self):
        # ID = f"{uuid.uuid4()}"
        ID = self.server_data["IP"].replace(".", "_")
        path_cons = os.path.join(os.getcwd(), f"connections")
        path_con = os.path.join(path_cons, self.country.lower())
        if not os.path.exists(path_cons):
            os.mkdir(path_cons)
            os.mkdir(path_con)
        elif not os.path.exists(path_con):
            os.mkdir(path_con)
        self.path_con_file = os.path.join(path_con, f"{ID}.ovpn")

        f = io.open(self.path_con_file, 'w', encoding="utf-8")
        f.write((base64.b64decode(self.server[-1])).decode("utf-8"))
        f.write('\nscript-security 2')
        f.close()

        f = io.open(os.path.join(path_con, f"{ID}.txt"), 'w', encoding="utf-8")
        for key, value in self.server_data.items():
            f.write(f'{key}: {value}\n')
        f.close()

    async def _async_run(self):
        self._get_server()
        self._create_con_file()
        self.process = subprocess.Popen(['bin/openvpn', '--config', self.path_con_file])

    def _background_run(self):
        self._get_server()
        self._create_con_file()
        self.process = subprocess.Popen(['bin/openvpn', '--config', self.path_con_file])

    def end(self):
        if self._as_thread:
            if self.thread is not None:
                self.thread.exit()
                self.thread = None
        else:
            if self.process is not None:
                self.process.kill()
                self.process = None

    def start(self):
        self._check_admin()
        self.loop.create_task(self._async_run())

    def run(self):
        self.start()
        self.loop.run_forever()

    def start_background(self):
        self.thread = threading.Thread(target=self._background_run)
        self.thread.daemon = True
        self.thread.start()

