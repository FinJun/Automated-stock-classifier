These files are for the final project of the Financial Software course in the Department of Financial Engineering at Ajou University. We used Kiwoom Securities' Open API to filter stocks based on criteria we set ourselves and recommend them, and then provide financial statements and news articles from the past month. The reason for using the API is not just to look up stock prices but to allow for the addition of more diverse functions tailored to user convenience in the future. Due to the limited project period, we could not add other functions, but it is possible to add various features such as buying and selling stocks and checking account balances using the API.

I will explain how to use the files and our code. Additionally, we will attach a Word file with various pictures to make it easier to apply in practice, so please refer to the Word file if you do not understand or if something does not execute correctly.

After downloading all the uploaded asda files, you should run the init file. Please make sure to install the open API and set up the Anaconda virtual environment before running.

After setting up the Open API usage and the 32-bit virtual environment, download the files we have uploaded and run the __init__.py file contained within those files. When running this program, you must forcibly set Anaconda to 32-bit, and it is crucial to set the interpreter correctly by creating a virtual environment with Python 3.7 during the virtual environment setup. If the Python version differs, there is a high likelihood of package setup issues, so we recommend using Python 3.7 within the virtual environment.

Once these settings are complete, you must actually install the Open API. Go to the Kiwoom Securities website, click on Open API, apply for and install the API. Then, install KOA Studio, which can unpack two files. Put these two files in the open API file on the C drive.

Since the Kiwoom Securities API is optimized for 32-bit, setting the environment is important. After installing Anaconda, open the cmd window and enter `set CONDA FORCE32BIT=1`. This step sets the Anaconda environment to 32-bit. Enter `conda create -n (desired name) python=3.7 anaconda`. This step creates a virtual environment with the name you want that includes Python 3.7. Now it will be installed. You can check the file path of the created virtual environment with `conda env list`. Activate it by entering `activate (set file name)`, then enter `python` to check if it is displayed as 32-bit. If the Python information is correctly displayed as 32-bit, you should set the python.exe file in that virtual environment file path as the interpreter.

We used SNS to verify various investment rationales and service intentions, finding that while people can easily access information, interpreting it and dealing with increasing amounts becomes challenging. Thus, we aimed to create a stock recommendation service for investors' convenience.
In the first stage, we selected stocks based on technical analysis, and in the second stage, we reselected them based on the industry PER. In the final stage, we brought up the last month's news (10 articles) and the stock names of the finally selected stocks.

In the first stage, we set criteria for appropriate charts. Our conclusion was to fetch charts of undervalued stocks that recently garnered market interest, which were stocks that had significantly increased trading volumes from a notably lower price state compared to past prices. After calling approximately 400 stocks with high fluctuations and trading volumes, we coded to find "golden cross stocks," which are trading significantly below the price 300 days ago with increased trading volume.

In the second stage, we crawled financial ratios from a site called Company Guide. The financial ratios on the Company Guide site are sequentially placed in `corp_group2>dl>dd`. We coded to pull these in order using the DOM tree structure.

In the last stage, we similarly crawled from Naver News and added a string of the stock name and n news articles (from the past month) to output them in sequence. 

Additionally, we will attach a Word file with various pictures to make it easier to apply in practice, so please refer to the Word file if you do not understand or if something does not execute correctly.!!!
