ADDRESSBOOK = {}

def input_error(wrap):
    def inner(*args):
        try:
            return wrap(*args)
        except IndexError:
            return "Please, give me name and phone"
        except KeyError:
            return "Contact not found. Please enter a valid name."
        except ValueError:
            return "Invalid input. Please enter a valid name and phone number."
        except TypeError as e:
            if "add_handler()" in str(e):
                return "Missing name and phone. Please provide both."
            raise e
    return inner

@input_error
def add_handler(name, phone):
    name = name.title()
    ADDRESSBOOK[name] = phone
    return f"Contact {name} with phone {phone} saved"


def exit_handler(*args):
    return "Good bye"

def enter_handler(*args):
    return "How can I help you?"

@input_error
def change_phone(name, phone):
    ADDRESSBOOK[name.title()] = phone
    return f"Phone number for contact {name} has been updated to {phone}."

@input_error
def get_phone(name):
    return f"The phone number for contact {name} is {ADDRESSBOOK[name.title()]}."

def show_all_contacts():
    if not ADDRESSBOOK:
        return "No contacts found."

    result = "Addressbook:\n"
    for name, phone in ADDRESSBOOK.items():
        result += f"{name}: {phone}\n"
    return result

def command_parser(raw_str: str):
    elements = raw_str.split()
    for func, keys in COMMANDS.items():
        if elements[0].lower() in keys:
            return func, elements[1:]

    return None, []

COMMANDS = {
    add_handler: ["add"],
    exit_handler: ["good bye", "close", "exit"],
    enter_handler: ["hello"],
    change_phone: ["change"],
    show_all_contacts: ["show", "show all", "show all contacts"],
    get_phone: ["get", "get phone"]
}


def main():
    while True:
        user_input = input(">>> ")
        if not user_input:
            continue
        func, data = command_parser(user_input)

        if func:
            if func == show_all_contacts:
                result = func()
            else:
                result = func(*data)
            print(result)
            if func == exit_handler:
                break
        else:
            print("Invalid command. Please try again.")

class Field:
    def __init__(self, value=None):
        self.value = value

    def edit(self, new_value):
        self.value = new_value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.edit(new_phone)
                break


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def __getitem__(self, name):
        return self.data[name]

    def find_records_by_name(self, name):
        return [record for record in self.data.values() if record.name.value == name]

    def find_records_by_phone(self, phone):
        return [record for record in self.data.values() if any(p.value == phone for p in record.phones)]


if __name__ == "__main__":
    name = Name('Bill')
    phone = Phone('1234567890')
    rec = Record(name)
    rec.add_phone(phone)
    ab = AddressBook()
    ab.add_record(rec)
    assert isinstance(ab['Bill'], Record)
    assert isinstance(ab['Bill'].name, Name)
    assert isinstance(ab['Bill'].phones, list)
    assert isinstance(ab['Bill'].phones[0], Phone)
    assert ab['Bill'].phones[0].value == '1234567890'
    print('All Ok)')