# python_dog.py
# This file defines the Dog class, which is a blueprint for creating dog objects.

class Dog:                                  # 1. CLASS: the blueprint. Names are Capitalized by convention.

    species = "Canis familiaris"            # 2. CLASS ATTRIBUTE: shared by EVERY dog. Same for all instances.

    def __init__(self, name, age):          # 3. CONSTRUCTOR: runs automatically when you make a new dog.
        self.name = name                    # 4. INSTANCE ATTRIBUTE: unique to THIS dog.
        self.age = age                      #    'self' means "this particular dog."
        self._hunger = 5                    # 5. underscore = "internal, please don't touch from outside."

    def bark(self):                         # 6. INSTANCE METHOD: an action a dog can do.
        return f"{self.name} says Woof!"

    def have_birthday(self):                # 7. Another method — this one CHANGES the dog's data.
        self.age += 1
        return f"{self.name} is now {self.age}."

    def __str__(self):                      # 8. DUNDER METHOD: controls how the dog looks when printed.
        return f"Dog(name={self.name}, age={self.age})"


def main() -> None:

    # ---- USING the class ----
    buddy = Dog("Buddy", 3)                 # 9. INSTANCE: one real dog built from the blueprint.
    print(buddy.name)                       # -> Buddy        (read an instance attribute)
    print(buddy.species)                    # -> Canis familiaris  (read the class attribute)
    print(buddy.bark())                     # -> Buddy says Woof!  (call a method)
    print(buddy.have_birthday())            # -> Buddy is now 4.
    print(buddy)                            # -> Dog(name=Buddy, age=4)  (uses __str__)

if __name__ == "__main__":  
    main()
