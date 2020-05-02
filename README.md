# Personal Budget

personal budget for daily record of transactions

## Getting Started

Download this repository to local machine

### Prerequisites

* python3
* mathplotlib.pyplot
* pandas
* csv

Install the required package with pip or conda, e.g.,

```
pip install csv
```
### Instruction
```
python3 script.py --h
usage: script.py [-h] [--add_transaction [ADD_TRANSACTION]]
                 [--set_budget [SET_BUDGET]] [--add_category [ADD_CATEGORY]]
                 [--pie [PIE]] [--bar [BAR]]

options

optional arguments:
  -h, --help            show this help message and exit
  --add_transaction [ADD_TRANSACTION]
                        add new transaction?
  --set_budget [SET_BUDGET]
                        set budget for different categories, e.g.(Medical,
                        200)
  --add_category [ADD_CATEGORY]
                        want to create a new category?
  --pie [PIE]           visualize in pie chart?
  --bar [BAR]           visualize in bar chart?
```


### Usage

Add a new transaction

```
python3 script.py --add_transaction
Date [yyyy-mm-dd]: 2020-01-15
Description: TK
Valid categories are
['Living', 'Insurance', 'Education', 'Other expenses', 'Travel', 'Utilities', 'Gifts', 'Food', 'Cosmetics', 'internship']
Category: Insurance
Amount: 100.00
```

Add a new category


```
python3 script.py --add_category
Current categories are
['Living', 'Insurance', 'Education', 'Other expenses', 'Travel', 'Utilities', 'Gifts', 'Food', 'Cosmetics', 'internship']
Do you still want to create a new category? [y/n]: y
New category: Sport
Do you want to set a budget for this category? [y/n]: n
```

Set a goal to the existing category

```
python3 script.py --set_budget
Valid categories are
['Living', 'Insurance', 'Education', 'Other expenses', 'Travel', 'Utilities', 'Gifts', 'Food', 'Cosmetics', 'internship', 'Sport']
For which category do you want to set the goal? [please choose one from the category-list above]: Sport
Please set a budget for the chosen category [a positive number]: 1
```

Visualize the monthly/annual expenses in pie chart
```
python3 script.py --pie
Please give a time window for visualization [yyyy or yyyy-mm]:  2020-02
```

Visualize the monthly/annual expenses in bar chart
```
python3 script.py --bar
Please give a time window for visualization [yyyy or yyyy-mm]:  2020-02
```



