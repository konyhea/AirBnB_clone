#!/usr/bin/python3

'''The console, entry point of the interpreter.'''

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User

# Dictionary of available classes
classes = {
    'BaseModel': BaseModel,
    'User': User
}


class HBNBCommand(cmd.Cmd):
    '''Entry point of your interpreter.'''
    prompt = '(hbnb) '

    def do_quit(self, line):
        '''Exit the program cleanly.'''
        return True

    def help_quit(self):
        print('Quit command to exit the program')

    def do_EOF(self, line):
        '''Terminate when EOF is reached.'''
        return True

    def help_EOF(self):
        print('Quit command to exit the program')

    def emptyline(self):
        pass

    def do_create(self, arg):
        '''Create a new instance of BaseModel.'''
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in classes:
            print("** class doesn't exist **")
            return
        new_instance = classes[class_name]()
        new_instance.save()
        print(new_instance.id)

    def help_create(self):
        print('Create a new instance of BaseModel or User')

    def do_show(self, arg):
        '''Show the string representation of an instance.'''
        args = arg.split()
        if len(args) == 0:
            print('** class name missing **')
            return
        class_name = args[0]
        if class_name not in classes:
            print('** class doesn\'t exist **')
            return

        if len(args) < 2:
            print('** instance id missing **')
            return
        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print('** no instance found **')
            return
        print(storage.all()[key])

    def help_show(self):
        print('Prints the string representation of an instance')

    def do_destroy(self, arg):
        '''Delete an instance based on the class name and id.'''
        args = arg.split()
        if len(args) == 0:
            print('** class name missing **')
            return
        class_name = args[0]
        if class_name not in classes:
            print('** class doesn\'t exist **')
            return
        if len(args) < 2:
            print('** instance id missing **')
            return
        key = f"{class_name}.{args[1]}"
        if key not in storage.all():
            print('** no instance found **')
            return
        del storage.all()[key]
        storage.save()

    def help_destroy(self):
        print('Deletes an instance based on the class name and id')

    def do_all(self, arg):
        '''Prints all string representation of all instances.'''
        args = arg.split()
        if args and args[0] not in classes:
            print('** class doesn\'t exist **')
            return
        if args:
            instances = [
                str(obj)
                for key, obj in storage.all().items()
                if key.startswith(args[0])
            ]
        else:
            instances = [str(obj) for obj in storage.all().values()]
        print(instances)

    def help_all(self):
        print('Prints all string representation of all instances.')

    def do_update(self, arg):
        '''Update an instance based on the class name or updating attribute.'''
        args = arg.split()
        if len(args) == 0:
            print('** class name missing **')
            return
        class_name = args[0]
        if class_name not in classes:
            print('** class doesn\'t exist **')
            return
        if len(args) == 1:
            print('** instance id missing **')
            return
        instance_id = args[1]
        key = f"{class_name}.{instance_id}"
        if key not in storage.all():
            print('** no instance found **')
            return
        if len(args) == 2:
            print('** attribute name missing **')
            return
        attribute_name = args[2]
        if len(args) == 3:
            print('** value missing **')
            return
        attribute_value = args[3].strip('"')
        instance = storage.all()[key]

        # Ensure id, created_at, updated_at can't be updated
        if attribute_name in ['id', 'created_at', 'updated_at']:
            print('** cannot update id, created_at, or updated_at **')
            return

        # Cast attribute value to appropriate type
        try:
            if hasattr(instance, attribute_name):
                attr_type = type(getattr(instance, attribute_name))
                attribute_value = attr_type(attribute_value)
            else:
                attribute_value = attribute_value
        except ValueError:
            print('** wrong type **')
            return

        setattr(instance, attribute_name, attribute_value)
        instance.save()

    def help_update(self):
        print('Updates an instance based on the class name or updating attr')


if __name__ == "__main__":
    HBNBCommand().cmdloop()
