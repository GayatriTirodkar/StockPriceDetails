# StockPriceDetails
A web scrapper to extract sector based company details. Build queries in SQL and Pandas to perform analysis on different parameters of the extracted data.

File Description:
1. all_companies_data.sql: The file is sql dump of total 6116 records for all the companies data that is parsed from https://www.moneycontrol.com/india/stockpricequote/ alphabets wise.
	The parameters parsed are:
		name of the company
		sector the company belongs to
		url
		nse number
		bse number
		isin number 
		market capital
		p/e ratio
		book value
		div percent
		market lot
		industry pe value
		eps ttm
		p/c
		price/book
		div yield percent
		face value
	

2. companies.csv: This is a simple csv file containing 6116 records of all companies data. Used for loading data for query execution and data retrival through Pandas.

3. companies_excluded.txt: Contains list of companies if any that were not parsed in one go due to unexpected response, redirection errors, timeouts etc.

4. data_extractor.py: Python script for data extraction. Required table if not exists in database is created and the extracted data is inserted in the table such a way that no duplicate enteries will be made even if script is executed multiple times.

5. pandas_query.py: This contains simple pandas query to tally the result of sql queries

6. sql_queries.txt: Sql  queries

7. Results of sql queries:
	a. third_highest_sector_wise.sql: Sql dump of result obtained for 3rd highest market capital sector wise

	b. fourth_highest_sector_wise.sql: Sql dump of result obtained for 4th highest market capital sector wise
	
	c. pe_ratio_buckets.sql: Sql dump obtained for forming bucket of P/E ratios in interval of 5, 11-15,16-20, 21-25,..., 66-70 

Command to import sql data:

	mysql -p -u [user] [database] < backup-file.sql

Please check data_extractor.py for details about the database connection.

