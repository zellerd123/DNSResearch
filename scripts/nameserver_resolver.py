from scripts import DNSResolver, ThreadPoolExecutor, json
'''
STEP 1 OF RESEARCH
Convert Domain name (from top 10k) --> NameServer
'''
class NameserverResolver(DNSResolver):
    def __init__(self, entry_limit : int = 10000, max_threads : int = 25):
        super().__init__(record_type = 'NS')
        self._entry_limit = entry_limit
        self._max_threads = max_threads
    
    
    def execute_nameserver_resolution(self):
        '''Executes Name Server Resolution'''
        # get top 10k domains from tranco list
        domains = self.read_csv(output_file_name = 'outputs/top-1m.csv', limit = self._entry_limit)
        
        # create thread pool executor to resolve name server for each domain
        with ThreadPoolExecutor(max_workers=self._max_threads) as executor:
            results = list(executor.map(self.resolve, domains))
        
        # We want to clean the results that returned 'None', which happens if error during resolution
        cleaned_results = self.drop_failed_resolutions(zip(domains, results))

        # write to JSON the output of our 10k nameserver resolutions.
        output_dict = {domain: nameservers for domain, nameservers in cleaned_results}
        with open('outputs/domains_nameservers.json', 'w') as jsonfile:
            json.dump(output_dict, jsonfile, indent=4)

        return self._resolution_failed_counter    