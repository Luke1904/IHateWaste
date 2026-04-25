# IHateWaste

A fully functional inventory analysis tool for business owners to better understand their enterprise with UI.


## Installation

#### 1.) Clone the Repository

```Python
git clone https://github.com/Luke1904/CP2_project.git
```

#### 2.) Install Dependencies

```Python
conda env create -f environment.yml 
```

#### 3.) Run Environment

```Python
conda activate your-env-name
```

#### ALL dependencies will be installed automatically onto your environment

## How to Run the Program

#### 1.) Make sure you have the environment installed and activated on your machine
#### 2.) Navigate to src/
#### 3.)Run the following command in windows powershell:
```Python
python -m PyInstaller --onefile --windowed main_gui.py

# The executable will be located in src/dist/
```







## Instructions

#### 1.) After the executable, you will now be given the option to browse and pick which file you intend to use for the program.
 *PLEASE NOTE FOR THE PROGRAM TO WORK YOU MUST USE AN EXCEL FILE*

#### 2.) After selecting desired files, click the option to clean the data or else the other features of the program will not become available

#### 3.) With the clean data you will now have the option of 5 choices to better help analyse your data to find trends and promote the best possible outcome for your business
## UI Features

#### 1.) Data Cleaning:

Cleaning the data will remove all nan values and check to make sure the file submitted is an excel file. In addiiton it filters all irrelevant data out

#### 2.) Average Income by Weekday:

Displays a bar graph in descending order relating to the average income per day

#### 3.) Holiday Earnings:

Displays two bar graghs with the left relating to aggregate earnings over holidays vs non-holidays. The right gragh relates to the average earnings over the holiday 

#### 4.) Most Popular Items:

Displays a bar gragh in descending order of the top 10 most purchased items

#### 5.) Volume of Items by Weekday:

Displays a bar gragh in descending order of the amount of items ordered each week calculated on a daily basis

#### 6.) Total Item Dispersion by Weekday:

Displays a table with three columns, titled: name item, day of the week and item volume by day respectively for every item available
## Usage

#### This program is intended for the user to optimise waste reduction and maximise profits. Examples of usage can be seen below

- Restaurant owners seeking to better understand their inventory and how it is used in each respective dish

- E-commerce, by using the program to better understand customer analytics
