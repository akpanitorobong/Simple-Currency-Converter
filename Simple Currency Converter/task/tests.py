from hstest import StageTest, CheckResult, dynamic_test, TestedProgram


class CurrencyConverter(StageTest):
    test_amounts = ["1", "3", "18", "50", "115"]
    usd = 1.0
    jpy = 113.50
    eur = 0.89
    rub = 74.36
    gbp = 0.75
    currencies = {"JPY": jpy, "EUR": eur, "RUB": rub, "GBP": gbp, "USD": usd}
    known_currencies = list(currencies.keys())
    test_data = []

    for i in range(0, len(test_amounts)):
        for j in range(0, len(known_currencies)):
            test_data.append([test_amounts[i], known_currencies[j], known_currencies[len(known_currencies) - 1 - j]])

    def convert_currency(self, amount, _from, to):
        _from = _from.upper()
        to = to.upper()
        result = int(amount) * self.currencies[to] / self.currencies[_from]
        format_result = "{:.4f}".format(result)
        return f"Result: {amount} {_from} equals {format_result} {to}"

    @dynamic_test
    def test1(self):
        main = TestedProgram()
        output = main.start()
        message = """Welcome to Currency Converter!
1 USD equals 1 USD
1 USD equals 113.5 JPY
1 USD equals 0.89 EUR
1 USD equals 74.36 RUB
1 USD equals 0.75 GBP
What do you want to do?
1-Convert currencies 2-Exit program
"""
        if message not in output:
            return CheckResult.wrong('Your output should be like in the example!')
        return CheckResult.correct()

    @dynamic_test(data=test_data)
    def test2(self, amounts, from_currency, to_currency):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            output = main.execute("1")
            message = "What do you want to convert?\nFrom:"
            if message not in output.strip():
                return CheckResult.wrong('You should ask for the "From" currency input like in the example!')
            output = main.execute(from_currency)
            message = "To:"
            if message not in output.strip():
                return CheckResult.wrong('You should ask for the "To" currency input!')
            output = main.execute(to_currency)
            message = "Amount:"
            if message not in output.strip():
                return CheckResult.wrong('You should ask for the "Amount" input!')
            output = main.execute(amounts)
            if self.convert_currency(amounts, from_currency, to_currency) not in output.strip():
                return CheckResult.wrong('You should output the correct result as in the example!')
            return CheckResult.correct()

        return CheckResult.wrong('You should give the user two options to choose from!')

    @dynamic_test()
    def test3(self):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            main.execute("1")
            output = main.execute("TL")
            message = "Unknown currency"
            if message not in output.strip():
                return CheckResult.wrong('You should output the correct message if an unknown input occurs.')
            elif main.is_finished() or not main.is_waiting_input():
                return CheckResult.wrong('Your program should resume and ask again after an unknown input!')
            return CheckResult.correct()
        return CheckResult.wrong('You should give the user two options to choose from!')

    @dynamic_test()
    def test4(self):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            main.execute("1")
            main.execute("USD")
            output = main.execute("This is a currency, believe me!")
            message = "Unknown currency"
            if message not in output.strip():
                return CheckResult.wrong('You should output the correct message if an unknown input occurs.')
            elif main.is_finished() or not main.is_waiting_input():
                return CheckResult.wrong('Your program should resume and ask again after an unknown input!')
            return CheckResult.correct()
        return CheckResult.wrong('You should give the user two options to choose from!')

    @dynamic_test(data=["-1", "a"])
    def test5(self, amount):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            main.execute("1")
            main.execute("USD")
            main.execute("GBP")
            output = main.execute(amount)
            message = "The amount cannot be less than 1"
            message2 = "The amount has to be a number"
            if amount == "-1" and message not in output.strip():
                return CheckResult.wrong('You should output the correct message if a negative amount is given.')
            elif amount == "a" and message2 not in output.strip():
                return CheckResult.wrong('You should output the correct message if a non-numeric amount is given.')
            elif  main.is_finished()  or not main.is_waiting_input():
                return CheckResult.wrong('Your program should resume and ask again after an unknown input!')
            return CheckResult.correct()

        return CheckResult.wrong('You should give the user two options to choose from!')

    @dynamic_test(data=["JpY", "jpy"])
    def test6(self, currency):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            main.execute("1")
            output = main.execute(currency)
            message = "To:"
            if message not in output.strip():
                return CheckResult.wrong('Your program should not be case sensitive!')

            output = main.execute(currency)
            message = "Amount:"
            if message not in output.strip():
                return CheckResult.wrong('Your program should not be case sensitive!')
            output = main.execute(self.test_amounts[1])
            if self.convert_currency(self.test_amounts[1], currency, currency) not in output.strip():
                return CheckResult.wrong('You should output the correct result as in the example!')
            return CheckResult.correct()

        return CheckResult.wrong('You should give the user two options to choose from!')

    @dynamic_test()
    def test7(self):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            output = main.execute("2")
            message = "Have a nice day!"
            if message not in output.strip():
                return CheckResult.wrong('You should output a goodbye message like in the example!')
            elif not main.is_finished():
                return CheckResult.wrong('Your program should finish after exiting!')
            return CheckResult.correct()

        return CheckResult.wrong('You should give the user two options to choose from!')

    @dynamic_test(data=["3", "a"])
    def test8(self, unknown_input):
        main = TestedProgram()
        main.start()
        if main.is_waiting_input():
            output = main.execute(unknown_input)
            message = "Unknown input"
            if message not in output.strip():
                return CheckResult.wrong('You should output a message like in the example if an unknown input occurs!')
            elif main.is_finished() or not main.is_waiting_input():
                return CheckResult.wrong('Your program should resume and ask again after an unknown input!')
            return CheckResult.correct()

        return CheckResult.wrong('You should give the user two options to choose from!')


if __name__ == '__main__':
    CurrencyConverter('main').run_tests()
