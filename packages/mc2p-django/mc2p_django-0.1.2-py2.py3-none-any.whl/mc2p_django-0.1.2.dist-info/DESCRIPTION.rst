# MyChoice2Pay Django


# Overview

MyChoice2Pay Django provides integration access to the MyChoice2Pay API through django framework.


# Requirements

* [Django][django]
* [MyChoice2Pay Python][mc2p-python]

# Installation

Install using `pip`...

    pip install mc2p-django

Add `'django_mc2p'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'django_mc2p',
        ...
    )

Add django_mc2p urls:

    urlpatterns = patterns('',
        ...
        url(r'^mc2p/', include('django_mc2p.urls'))
        ...
    )

# Configuration

After execute migrations you must define KEY and SECRET KEY in administration site, section MyChoice2Pay Configuration.

You can obtain KEY and SECRET KEY from [MyChoice2Pay][mychoice2pay-site] site.

# Quick Example

### Basic transaction

    # Sending user to pay
    from django_mc2p import MC2PClient

    mc2p = MC2PClient()
    transaction = mc2p.Transaction({
        "currency": "EUR",
        "order_id": "order id",
        "products": [{
            "amount": 1,
            "product": {
                "name": "Product",
                "price": 50
            }
        }],
        "notify_url": "https://www.example.com" + reverse('mc2p-notify'),
        "return_url": "https://www.example.com/your-return-url/",
        "cancel_return": "https://www.example.com/your-cancel-url/"
    })
    transaction.save()
    transaction.pay_url # Send user to this url to pay

    # After user pay a notification will be sent to notify_url
    from django_mc2p.constants import MC2P_PAYMENT_DONE
    from django_mc2p.signals import notification_received

    def check_payment(sender, **kwargs):
        notification_data = sender
        if notification_data.type == MC2P_TYPE_TRANSACTION and notification_data.status == MC2P_PAYMENT_DONE:
            transaction = notification_data.transaction
            sale = notification_data.sale
            order_id = notification_data.order_id
            # Use transaction, sale and order_id to check all the data and confirm the payment in your system
    notification_received.connect(check_payment)

### Basic subscription

    # Sending user to pay a subscription
    from django_mc2p import MC2PClient

    mc2p = MC2PClient()
    subscription = mc2p.Subscription({
        "currency": "EUR",
        "order_id": "order id",
        "plan": {
            "name": "Plan",
            "price": 5,
            "duration": 1,
            "unit": "M",
            "recurring": true
        },
        "notify_url": "https://www.example.com" + reverse('mc2p-notify'),
        "return_url": "https://www.example.com/your-return-url/",
        "cancel_return": "https://www.example.com/your-cancel-url/"
    })
    subscription.save()
    subscription.pay_url # Send user to this url to pay

    # After user pay a notification will be sent to notify_url
    from django_mc2p.constants import MC2P_PAYMENT_DONE
    from django_mc2p.signals import notification_received

    def check_payment(sender, **kwargs):
        notification_data = sender
        if notification_data.type == MC2P_TYPE_SUBSCRIPTION and notification_data.status == MC2P_PAYMENT_DONE:
            subscription = notification_data.subscription
            sale = notification_data.sale
            order_id = notification_data.order_id
            # Use subscription, sale and order_id to check all the data and confirm the payment in your system
    notification_received.connect(check_payment)

[django]: https://www.djangoproject.com/
[mc2p-python]: https://github.com/mc2p/mc2p-python
[mychoice2pay-site]: https://www.mychoice2pay.com/


