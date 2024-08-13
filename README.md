

## Measuring Consolidation of DNS and Percentage of In-Bailiwick Servers






## Experiment Replication Methodology

To replicate the experiment, execute the following command in your terminal:

`python3 run.py`


You can customize the experiment with optional parameters:

- `-t` to specify the number of threads for faster results generation (default is 25).
- `-r` to set the number of domains from the Tranco top 1M list to use (default is 10k).

`run.py` orchestrates the experiment by calling scripts from the `/scripts` directory, each extending the `DNSResolver` base class in `dns_resolver.py`.

Running `run.py` with 25 threads on 10k domains takes approximately 4 minutes to complete all steps of the experiment.
### Needed Packages
Install matplotlib and numpy

### Steps

1. `NameserverResolver`: Resolves NS records the top N domains specified by the `-r` parameter. Outputs to `/outputs/domain_nameservers.json`.
2. `IPResolver`: Resolves A records for nameservers from Step 1. Outputs to `/outputs/nameserver_ips.json`.
3. `ASNResolver`: Acquires Autonomous System Numbers for each IP from Step 2. Outputs to `/outputs/ip_to_asn_mapping.json`.
4. `AS_Org_Resolver`: Obtains AS Organization for each ASN from Step 3. Outputs to `/outputs/asn_to_org_mapping.json`.

After data collection:

5. `ProcessResults`: Analyzes the collected data to identify top unreachable/affected domains and Inbailwick domains. Outputs to `/outputs/results.json`.
6. `PresentResults`: Visualizes the processed data with graphics. Outputs to `/graphics` folder.


## Results from Experiment Replication

Our replication experiment revealed a significant concentration in the hosting of domain name servers, with Amazon and Cloudflare alone being responsible for the exclusive hosting of 47.9% of domains. This marks a noticeable increase compared to the original study's findings, where these two organizations accounted for 37% of domain hosting. Overall, the top ten most popular name server hosting providers now contribute to the reachability of 61.9% of domains, up from 50.7% noted in the original study. This 11% rise shows a growing consolidation in the market for name server hosting services.

The outcomes of our study are visually represented in the following figures:

**Figure 1: Number of Domains Exclusively Using One AS for Name Servers (Unreachable) vs. Partially Using One AS (Affected)**

![Number of Domains Analysis](/graphics/bar_chart.png)

**Figure 2: Percentages of Domains Exclusively Using One AS Organization for Name Servers (Unreachable) vs. Partially Using One AS (Affected)**

![AS Organization Analysis](/graphics/result_table.png)

## Domains that could not be processed: 


**Step 1: Executing Nameserver Resolution**

  Failed NS Resolutions: 110

  
**Step 2: Executing IP Resolution for Nameservers**

  Failed A Resolutions: 179

  
 **Step 3: Executing ASN Resolution for IPs**

  Failed TXT Resolutions: 22

  
**Step 4: Executing AS Org Resolution for ASNs**

  Failed TXT Resolutions: 0


## Inbailwick Methodology

Our analysis extended to the domain of Inbailwick consolidation, which occurs when a name server operates as a subdomain of the domain it is designated to serve — for example, ns1.example.com is considered Inbailwick for example.com. We define a domain as 'completely Inbailwick' when all its name servers are a subdomain of the domain it serves. Conversely, a 'partially Inbailwick' classification is applied to domains with at least one, but not all, name servers hosted by the same organization. 

To do this, we processed the existing output data from our experiment replication. No additional data generation was required; we reanalyzed the initially gathered data under a new lens for the Inbailwick portion of our study. All results regarding Inbailwick servers are generated when `run.py` is executed.

## Inbailwick Results

The Inbailwick analysis points out that it's becoming rare to find domains that are fully inbailwick, meaning the domain and its nameservers are on the same domain. It seems like more and more domain hosting is getting scooped up by a few big companies. This centralization could be a problem because it puts too much control in the hands of a few companies, which might limit options and increase costs for everyone else.

**Figure 3: Percentage of Domains Completely Inbailwick vs. Partially Inbailwick**

![Inbailwick Analysis](/graphics/inbailwick_table.png)

### ERRORS

As described in our methodology, our inbailwick data collection used the intermediate outputs from the experiment replication. Therefore, the errors are the same as the ones seen above.

