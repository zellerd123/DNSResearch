import csv
import json
from concurrent.futures import ThreadPoolExecutor
import dns.resolver
from typing import List, Dict

'''Base Class for all DNS Resolvers to replicate experiment'''
class DNSResolver:
    def __init__(self, record_type : str):
        '''When initalized, must specify a record type that is being parsed for experiment
        
        @Keyword arguments: 
        record_type(str): specifies type of record type
        
        '''
        self._resolver = dns.resolver.Resolver()
        self._resolver.nameservers = ['127.0.0.1']
        self._resolver.port = 8053
        self._resolution_failed_counter = 0
        self._record_type = record_type

    
    def resolve(self, query : str) -> str:
        '''
        General Resolve Function. Query parameter will vary based 
        on what sub class functionality is & what self._record_type is.
        
        @Keyword arguments:
        query(str): The DNS query to resolve
        '''
        try:
            answer = self._resolver.resolve(query, self._record_type)
            if self._record_type == 'NS':
                return [str(a) for a in answer]
            elif self._record_type == 'A' or self._record_type == 'TXT':
                return str(answer[0])
            else:
                raise Exception(f'Record Type: {self._record_type} not supported.')
        except Exception as e:
            self._resolution_failed_counter += 1
            return None

    
    def drop_failed_resolutions(self, domain_pairs: List[tuple]) -> List[tuple]:
        '''
        Helper function to drop any failed resolutions 
        (if resolution raised an error, resulting in it returning None)
        
        @Keyword arguments: 
        domain_pairs(List[tuple]): A list of domain, resolution pairs to filter
        '''
        # Filter out pairs where the the value of entry is None
        return [pair for pair in domain_pairs if pair[1] is not None]

    
    def read_csv(self, output_file_name : str, limit : int = 10000) -> List[str]:
        '''
        Reads and returns list of str from CSV output. 
        This helper function is used to read top 10k
        
        @Keyword arguments: 
        output_file_name(str): Name of requested file to unpack
        limit(int): Number of lines to read and store
        '''
        results : List[str] = []
        with open(output_file_name, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for i, row in enumerate(csvreader):
                if i >= limit: 
                    break
                results.append(row[1])
        return results

    
    def read_json(self, output_file_name : str) -> Dict:
        '''
        Reads JSON outputs from previous results
        
        @Keyword arguments:
        output_file_name(str): Name of requested file to unpack
        '''
        with open(output_file_name, 'r') as jsonfile:
            data = json.load(jsonfile)
        return data