Fig's accountancy tool

Management of accountancy in command line.
  - Double entry accounting
  - Allows you to register entries in CSV format (via spreadsheet)
  - Manages repetitive patterns
  - Reads HSBC statements and transforms them into bookkeeping entries
  - Generates Journal, General Ledger, Balance sheet and Income statements
  - Closes the year and retrieves the entries to open the new year
  - Understands French corporate taxes and social contributions
  - Reads calendar delivery entries for consulting company in order to:
      - generate PDF bill from latex template
      - enter billing in accounts
  - Localized in French and English (to be improved)

- Initialize system for a new entity (company, personal accounts...):
    python facct/init_year.py -o company_name_or_alias -c
    #Note that the accountancy will initialize for the current year.

- Initialize the accounts for a new year:
    python facct/init_year.py -o company_name_or_alias -y 2014

- Generate a bill for February 2013:
    python facct/bill/gen_tex.py 022013.csv -o titu
    #If the file does not exists, it will generate 022013.csv in
     ${bills}/022013.csv with all the work days filled in to 1.
     If you want to change values replace 1 by 0 to indicate off days or
     to change by something other than an integer 0.75, you will to
     relaunch the command to generate the PDF bill.

- Configuration file:
   The facct configuration file is located in ~/.facct.rc, it's a simple
   INI file, feel free to change some locations if you want.
   You should also change values for the following files located in $data:
    - contracts.csv    : some basic info about contracts
    - bank_accounts.csv: bank account details
    - clients.csv      : client details
    - company.csv      : company (or personal) details, the minimum needed.

- To regenerate accountancy after some modifications (new bill, new expense):
    python facct/generate_all.py -o titu -d $accounts/<year>

- To modify some entries, you can change the input file:
    ./accounts/<year>/journal.ori.csv
    # You can use some templates such as those you can find for example in
    the file <path_to_app>/facct/bench/accounts/<one_year>/journal.ori.csv.

- Developer feature:
  You can launch some benchmarks with:
    ./scripts/bench.sh

- Workflow:
                   journal.ori.csv
                         |
                         |-------<---- [bills/<year>/except.txt]
                         |
                         V
                   journal_tmpl.csv
                         |
                         |
                         V
                  (unroll templates)
                         V
                         |
                         |-------<---- [hsbc/*.csv]
                         |
                         V
                     <year>.csv      <-- journal
                         |
                         |
                         V
                     <year>.gl.csv   <-- General Ledger
                        /   \
                       /     \
                      |       |
                      V       V
                Balance       Income statements

