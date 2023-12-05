from .models import House, RentRecord


def get_balance(house_id, amount_paid):
    house = House.objects.get(id=house_id)
    record = RentRecord.objects.filter(house=house).order_by('-id').first()
    if record:
        current_balance = record.balance
    else:
        current_balance = 0
    rent = house.rent
    if current_balance == 0:
        new_balance = rent - amount_paid
    else:
        new_balance = current_balance - amount_paid

    return new_balance
