from scripts import DNSResolver, ThreadPoolExecutor, json

'''
STEP 2 OF RESEARCH
Convert Name Server --> IP Address
'''
class IPResolver(DNSResolver):
    def __init__(self, max_threads : int = 25):
        super().__init__(record_type = 'A')
        self._max_threads = max_threads

    
    def execute_ip_resolution(self):
        '''Executes IP Resolution from results of Nameserver Resolution'''
        # cleans output of json so we just have list of nameservers.
        nameservers : List[List[str]] = list(self.read_json(output_file_name = 'outputs/domains_nameservers.json').values())

        # flattens the space of nameservers so we have one giant list of all nameservers.
        flattened_nameservers : List[str] = [ns for sublist in nameservers for ns in sublist]

        # create thread pool executor to resolve ip of each nameserver
        with ThreadPoolExecutor(max_workers=self._max_threads) as executor:
            results = list(executor.map(self.resolve, flattened_nameservers))

        # Clean results of IP resolution from nameservers.
        cleaned_results = self.drop_failed_resolutions(zip(flattened_nameservers, results))

        # Create a dictionary from the cleaned results
        nameserver_to_ip = {nameserver: ip for nameserver, ip in cleaned_results}

        # Write to JSON the output of IP resolutions
        with open('outputs/nameserver_ips.json', 'w') as jsonfile:
            json.dump(nameserver_to_ip, jsonfile, indent=4)
        return self._resolution_failed_counter
