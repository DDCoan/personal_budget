import csv
import pandas as pd
import argparse
import locale
import datetime
import matplotlib.pyplot as plt
import locale
import numpy as np
import os.path
import seaborn as sns
from sys import exit

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
plt.style.use('seaborn')

###############################################
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def check_year_month_day(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

###############################################
parser = argparse.ArgumentParser(description='options')
parser.add_argument("--add_transaction", type=str2bool, nargs='?',
                        const=True, default=False,
                        help='add new transaction?')
parser.add_argument('--set_budget', type=str2bool, nargs='?',
                    const=True, default=False,
                    help='set budget for different categories, e.g.(Medical, 200)') 
parser.add_argument('--add_category', type=str2bool, nargs='?',
                        const=True, default=False, 
                        help='want to create a new category?')
parser.add_argument("--pie", type=str2bool, nargs='?',
                        const=True, default=False, 
                        help='visualize in pie chart?')
parser.add_argument('--bar', type=str2bool, nargs='?',
                        const=True, default=False, help='visualize in bar chart?')

args = parser.parse_args()

###############################################

class PersonalBudget(object):
    def __init__(self):
        self.category_path = 'categories_budget.csv'
        self.record_path = 'record.csv'
        category_exists = os.path.isfile(self.category_path) 
        if not category_exists:
            with open(self.category_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['category', 'budget'])
        self.cat_budget = pd.read_csv(self.category_path)
            
        
        record_exists = os.path.isfile(self.record_path)
        if not record_exists:
            with open(self.record_path, 'w') as file:
                writer = csv.writer(file)
                writer.writerow(['date','description','category','amount'])
        self.record = pd.read_csv(self.record_path)
            

    def add_transaction(self):
        cats = list(self.cat_budget['category'])

        date = input('Date [yyyy-mm-dd]: ')
        while not check_year_month_day(date):
            date = input('Invalid input, please re-enter date [yyyy-mm-dd]: ')
    
        des = input('Description: ')
        print('Valid categories are \n' + str(cats))
        cat = input('Category: ')
        while cat not in cats:
            cat = input('Invalid category, please choose one from the list above: ')
        amount = input('Amount: ')

        with open(self.record_path, 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, des, cat, amount])
    
    def add_category(self):
        cats = list(self.cat_budget['category'])
        print('Current categories are \n' + str(cats))
        inp = input('Do you still want to create a new category? [y/n]: ')
        if inp =='y':
            new_cat = input('New category: ')
            while new_cat in cats:
                new_cat = input('This category already exists, please choose another one: ')
            answer = input('Do you want to set a budget for this category? [y/n]: ')
            if answer == 'y':
                budget = input('please set a goal for the chosen category [a positive number]: ')
            else:
                budget = 0.        
            with open(self.category_path, 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([new_cat, budget]) 

    def set_budget(self):
        cats = list(self.cat_budget['category'])
        print('Valid categories are \n' + str(cats))
        cat_to_set = input('For which category do you want to set the goal? [please choose one from the category-list above]: ')
        while cat_to_set not in cats:
            cat_to_set = input('Invalid catgory , please choose one from the category-list above: ')
        budget = input('Please set a budget for the chosen category [a positive number]: ')
        while int(budget) < 0.:
            budget = input('please input a positive number as budget: ')
        self.cat_budget.loc[(cat_to_set == self.cat_budget['category']), ['budget']] = budget
        self.cat_budget.to_csv(self.category_path, index=False)

    def date_mask(self, time_window):
        if len(time_window) == 4:
            mask = (pd.DatetimeIndex(self.record['date']).year == int(time_window))
        else:
            mask = (
                    (pd.DatetimeIndex(self.record['date']).year == int(time_window[:4]))
                    &
                    (pd.DatetimeIndex(self.record['date']).month == int(time_window[-2:]))
                    )
        return mask
        

    def pie_plot(self):
        # check validity of the time window
        time_window = input("Please give a time window for visualization [yyyy or yyyy-mm]:  ")

        while not self.date_mask(time_window).any():
            time_window = input("No records for the given time window, please reinput [yyyy or yyyy-mm]:  ")

        mask = self.date_mask(time_window)

        df = self.record.copy()

        df = df.loc[mask]
        print(df)

        print('In total: {:.2f}'.format(df['amount'].sum()))
        df.groupby(['category']).sum().plot.pie(y='amount', autopct= lambda a: '{:.2f}%'.format(a), cmap='Set2').legend(loc='best',bbox_to_anchor=(1.0, 1.0))
         #, wedgeprops={'alpha':0.6}
        plt.tight_layout()
        plt.show()


    def bar_plot(self):
        # check validity of the time window
        time_window = input("Please give a time window for visualization [yyyy or yyyy-mm]:  ")
        # self.record = pd.read_csv(self.record_path)

        while not self.date_mask(time_window).any():
            time_window = input("No records for the given time window, please reinput [yyyy or yyyy-mm]:  ")
        mask = self.date_mask(time_window)

        df = self.cat_budget.copy()
        record = self.record.loc[mask]

        # budget * 12 for one year
        if len(time_window) == 4:
            print('hi')
            df['budget'] = 12 * df['budget']
        actual = record.groupby(['category'], as_index = False)['amount'].sum()
        df = df.merge(actual, how='left', on= 'category') 
        
        df.fillna(0, inplace=True)

        df2 = df.replace('amount','actual', inplace=True)
        print(df2)

        print('Budget in total: {:.2f}'.format(df['budget'].sum()))
        print('Actual in total: {:.2f}'.format(record['amount'].sum()))
        
        df = df.melt(id_vars=["category"], 
                  var_name="type", value_name="amount")
        df.replace('amount','actual', inplace=True)
        g = sns.catplot(x="category", y="amount", hue="type", data=df,
                        height=6, kind="bar", palette='Set2',legend=False, aspect=1.5)
        # g.despine(left=True)
        g.set_ylabels("Comparasion between Budget and Actual")
        plt.legend(frameon=True)
        plt.show()



if __name__ == '__main__':
    # titanic = sns.load_dataset("titanic")
    pb = PersonalBudget()

    if args.add_category:
        pb.add_category()

    if args.add_transaction:
        pb.add_transaction()

    if args.set_budget:
        pb.set_budget()

    if args.pie:
        pb.pie_plot()

    if args.bar:
        pb.bar_plot()





