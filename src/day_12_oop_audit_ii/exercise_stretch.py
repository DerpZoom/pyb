"""
day_12_oop_audit_ii/exercise.py --> stretch goal
 
OOP audit II: composition over inheritance, and the dunders
you will actually reach for on the job.
"""


from dataclasses import dataclass
from typing import Iterator


@dataclass
class Sensor:
    """A single field device: a tag name and its last reading."""
    tag: str
    reading: float
    units: str = "eng"
 
    def __eq__(self, other: object) -> bool:
        # Two readings are "equal" if tag + reading + units match --
        # NOT if they are the same object in memory. This is what == should
        # mean for a data-like class (contrast with `is`, which checks identity).
        if not isinstance(other, Sensor):
            return NotImplemented  # let Python try the other side, don't crash
        return (self.tag, self.reading, self.units) == (other.tag, other.reading, other.units)
 
 
class SensorArray:
    """
    A COMPOSED collection of sensors. This class HAS sensors -- it does
    NOT inherit from Sensor. A SensorArray is not "a kind of" Sensor, so
    subclassing here would model the wrong relationship (see WHAT JUST
    HAPPENED below for why that distinction matters in practice).
    """
 
    def __init__(self, name: str) -> None:
        self.name = name
        self._sensors: list[Sensor] = []  # composition: array HAS-A list of sensors
 
    def add(self, sensor: Sensor) -> None:
        self._sensors.append(sensor)
 
    def __len__(self) -> int:
        # Enables len(array) -- the dunder behind the len() builtin.
        return len(self._sensors)
 
    def __iter__(self) -> Iterator[Sensor]:
        # Enables "for sensor in array:" -- the iteration protocol.
        return iter(self._sensors)
 
    def __getitem__(self, index: int) -> Sensor:
        # Enables array[0] -- the indexing / subscript protocol.
        return self._sensors[index]
 
    def __contains__(self, tag: str) -> bool:
        # ??? implement so `"TT-101" in array` works, matching by tag name
        for sensor in self._sensors:
            if sensor.tag == tag:
                return True
        return False

    def __repr__(self) -> str:
        return f"SensorArray(name={self.name!r}, sensors={len(self._sensors)})"

    def __add__ (self, other: "SensorArray") -> "SensorArray":
        # Enables array1 + array2 -- the addition protocol.
        if not isinstance(other, SensorArray):
            return NotImplemented
        new_array = SensorArray(name=f"{self.name} + {other.name}")
        new_array._sensors = self._sensors + other._sensors
        return new_array
 
def main() -> None:
    array = SensorArray("Line 3 Skid")
    array.add(Sensor(tag="TT-101", reading=72.4, units="degF"))
    array.add(Sensor(tag="PT-201", reading=14.7, units="psi"))
    array.add(Sensor(tag="FT-301", reading=88.0, units="gpm"))

    print("-" * 40)
 
    print(f"{len(array)} sensors on {array.name}")
    for sensor in array:
        print(f"  {sensor}")

    print("-" * 40)
 
    print(f"array[0] -> {array[0]}")
    print(f"'PT-201' in array -> {'PT-201' in array}")
    print(f"'ZZ-999' in array -> {'ZZ-999' in array}")

    print("-" * 40)
 
    a = Sensor(tag="TT-101", reading=72.4, units="degF")
    b = Sensor(tag="TT-101", reading=72.4, units="degF")
    print(f"a == b -> {a == b}   (same values, different objects)")
    print(f"a is b -> {a is b}   (identity, not equality)")

    print("-" * 40)

    array2 = SensorArray("Line 4 Skid")
    array2.add(Sensor(tag="TT-102", reading=272.4, units="degF"))
    array2.add(Sensor(tag="PT-202", reading=214.7, units="psi"))
    array2.add(Sensor(tag="FT-302", reading=288.0, units="gpm"))

    array3 = array + array2
    print(f"array3 -> {array3}")

    print("-" * 40)

    print(f"{len(array3)} sensors on {array3.name}")
    for sensor in array3:
        print(f"  {sensor}")

    print("-" * 40)

if __name__ == "__main__":
    main()
