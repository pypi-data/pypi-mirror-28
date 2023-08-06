Usage: gdax_recurring [OPTIONS]

  This script automates recurring USD deposits and asset allocation for
  GDAX.

  When run, it will check whether a deposit needs to be made and, if so,
  initiate the deposit using a linked bank account.

  Then, if there is enough available USD in the GDAX account, it will buy
  currencies using all of the available USD, given a user-specified asset
  allocation. Currencies are traded at market price at the time the script
  is run.

  This script is meant to be run as a cron. The cron can be run at any
  interval less than the `deposit-interval` -- I recommend daily. The script
  will ensure that deposits are only made every `deposit-interval`
  irrespective of how often it is run. Please make sure that only one
  instance of gdax_recurring is running at a time to prevent duplicate
  deposits.

  In addition to the CLI options, a few environment variables must be
  present:

      GDAX_API_KEY
      GDAX_API_SECRET
      GDAX_PASSPHRASE

  Installation:

      pip install gdax_recurring

  Example usage:

      export GDAX_API_KEY=<your_api_key>
      export GDAX_API_SECRET=<your_api_secret>
      export GDAX_PASSPHRASE=<your_passphrase>
      gdax_recurring -d 100.00 -i 15 -m 50.00 -a LTC 0.5 -a ETH 0.25 -a BTC 0.25

  Explanation:

      The above invocation will deposit $100.00 every 15 days. In addition,
      if the GDAX account has at least $50.00 available to trade, all of the
      available USD will be used to buy other currencies as follows:

      50% will be used to buy LTC
      25% will be used to buy ETH
      25% will be used to buy BTC

Options:
  -d, --deposit-amount TEXT       Amount to deposit every `deposit-interval`
                                  days
  -i, --deposit-interval INTEGER  Interval in days after which a deposit
                                  should be made
  -m, --min-available-to-trade DECIMAL
                                  The minimum available balance in USD that,
                                  when met, will result in an allocation
  -a, --allocation-percentage <TEXT DECIMAL>...
                                  A currency and the percentage of available
                                  funds that should be allocated to it. This
                                  option may be provided multiple times for
                                  different currencies and the total
                                  percentage should add up to 1. If the total
                                  percentage is less than one, the remainder
                                  will be left as USD. 

                                  Example: -a ETH 0.25
                                  -a BTC 0.25 -a LTC 0.5
  -h, --help                      Show this message and exit.


