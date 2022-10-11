from dataclasses import dataclass
from typing import List
from sys import argv


@dataclass
class PowerTenDecompositionItem:
    weight: int
    power_ten: int
    minus_power_ten: int | None = None


class RomanNumerals:
    ## These values are basic
    _ROMAN_NUMERAL_SYMBOLS = {
        1: 'I',
        5: 'V',
        10: 'X',
        50: 'L',
        100: 'C',
        500: 'D',
        1000: 'M'
    }

    ## This function return the power of ten
    ## of a given number retrieve in our 
    ## Roman numeral symbols keys 
    ## E.g:
    ## For 3000, we should return 1000
    ## For 80, we should return 10
    ## For 400000, we should return 1000 (
    # because in roman numeral symbols
    # biggest power of ten number is 1000)
    @staticmethod
    def get_power_of_ten(number: int) -> int:
        power = len(str(number)) - 1
        # don't forget in roman numeral symbols
        # the biggest power of ten is 10^3 = 1000
        power = min(power, 3)
        return 10**power
    
    ## This function returns the decomposition of a number
    ## in power of ten.
    ## NB: Because our highest power of ten in roman symbols is 1000
    ## 1000 would be our highest power of ten on this decomposition
    @staticmethod
    def get_decomposition_on_power_of_ten(number: int) -> List['PowerTenDecompositionItem']:
        rest_of_division = number
        result = []
        while rest_of_division != 0:
            power_ten = RomanNumerals.get_power_of_ten(rest_of_division)
            result.append(PowerTenDecompositionItem(rest_of_division//power_ten, power_ten))
            rest_of_division %= power_ten
        return result
    
    ## This function returns the decomposition of a given number
    ## This decomposition should be related to roman symbols fixed values
    @staticmethod
    def get_roman_numeric_decomposition(number: int) -> List['PowerTenDecompositionItem']:
        power_ten_decomposition = RomanNumerals.get_decomposition_on_power_of_ten(number)
        result = []
        for item in power_ten_decomposition:
            if item.power_ten == 1000:
                result.append(item)
            elif item.weight == 9:
                result.append(PowerTenDecompositionItem(
                    1, item.power_ten * 10, item.power_ten
                ))
            elif item.weight == 4:
                result.append(PowerTenDecompositionItem(
                    1, item.power_ten * 5, item.power_ten * 5
                ))
            elif item.weight >= 5:
                result.append(PowerTenDecompositionItem(1, item.power_ten * 5))
                result.append(PowerTenDecompositionItem(item.weight - 5, item.power_ten))
            else:
                result.append(item)
        return result

    ## This function get the roman number
    ## from the numeric given number
    @staticmethod
    def compute_roman_number(numeric_number: int) -> str:
        # Make sure the given number is stricly positive
        if numeric_number <= 0:
            return ''
        # Decompose the given number 
        decomposition = RomanNumerals.get_roman_numeric_decomposition(numeric_number)
        result = ""
        for item in decomposition:
            item_format = ""
            if item.minus_power_ten:
                item_format = RomanNumerals._ROMAN_NUMERAL_SYMBOLS[item.minus_power_ten]
            item_format += RomanNumerals._ROMAN_NUMERAL_SYMBOLS[item.power_ten] * item.weight
            result += item_format
        return result


def main(arguments):
    '''
    This function returns the roman numbers of the given numeric numbers.
    $ python roman_numerals [numb_1] [numb_2] ... [numb_n]
    '''

    if len(set(arguments) & {"-H", "-h", "--help"}) != 0:
        print(main.__doc__)
        return
    try:
        numbers = [int(arg) for arg in arguments]
    except ValueError:
        print("Uniquement les nombres entiers sont requis")
        return
    for number in numbers:
        print("%s => %s" % (number, RomanNumerals.compute_roman_number(number)))


if __name__ == "__main__":
    main(argv[1:])
    
    