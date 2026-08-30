# python_pet_shelter.py
# This file imports the Dog class from python_dog.py and uses it.

from python_dog import Dog          # grab ONLY the Dog class out of python_dog.py
                                    # Because of the __main__ guard in python_ dog.py,
                                    # Buddy's demo does NOT print when we import.

def main() -> None:
    # Build a few dogs from the imported blueprint
    shelter = [
        Dog("Rex", 2),
        Dog("Luna", 5),
        Dog("Pepper", 1),
    ]

    print(f"We have {len(shelter)} dogs available:\n")

    for dog in shelter:              # loop over each dog
        print(dog)                   # uses __str__ -> Dog(name=..., age=...)
        print("   ", dog.bark())     # call a method on that dog
        print("   ", dog.have_birthday())
        print()                      # blank line between dogs

    # Class attribute is shared by all of them
    print("All dogs are the species:", Dog.species)


if __name__ == "__main__":
    main()