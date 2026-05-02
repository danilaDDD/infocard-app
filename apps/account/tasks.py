from celery import shared_task


@shared_task
def log_new_account(account_id: int) -> None:
    from apps.account.models import Account

    account = Account.objects.filter(id=account_id).first()
    if account is None:
        return

    print(f'New account registered: id={account.id}, username={account.username}, email={account.email}')