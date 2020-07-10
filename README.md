# Panera_Coffee
Free Panera coffee at the click of a button (for summer 2020). This is a simple selenium script meant to demonstrate how to interact with chromium web browser.

## Getting Started

Create account at [panera](https://www.panerabread.com/en-us/mypanera/mypanera-coffee-subscription.html) and enter credit information. Panera has waived the fee for the summer, but still requires you to make a subscription account––which requires your credit card. After you enter this you can cancel your subscription and continue the benefits of free coffee for the summer. Don't forget to cancel you subscription when summer ends or you'll be charged.

### Prerequisites

What things you need to install the software and how to install them

```
pip install selenium
```

### Installing

Download zip repo and unzip your specific chromedriver zip file

## Execution

Drinks currently offered for free from Panera are: Iced Coffee | Light Roast Coffee | Hazelnut Coffee | Dark Roast Coffee | Decaf Coffee | Hot Tea

```
python main.py --username <your panera email> --password <your panera password> --zip <your store zip code> --type <your panera drink name>
```

## Authors

**Benjamin Hobson**

See also the list of [contributors](https://github.com/bjhobson12/Panera_Coffee/contributors) who participated in this project.

## Liability

Use this repo at your own risk. I do not assume liability in any way for this program; it is a simple demonstration of Selenium technology, used to order a coffee from Panera. This project was created independent of [Panera Bread](https://www.panerabread.com).
