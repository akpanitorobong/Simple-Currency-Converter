let input = require('sync-input');

const rateMap = new Map([
    ["USD",1],
    ["JPY",113.5],
    ["EUR",0.89],
    ["RUB",74.36],
    ["GBP",0.75]
]);
//FUNCTIONS
//Welcome and Display rates
function displayRates()
{
    console.log("Welcome to Currency Converter!");
    rateMap.forEach((rate,currency)=>
    {
        console.log("1 USD equals "+rate+" "+currency);
    });
}

//Loop when there is an error in input or a conversion is completed
function whatDoYouWantToDo()
{
    let looping = 1;
    while(looping)
    {
        console.log("What do you want to do?");
        let toDo = input("1-Convert currencies 2-Exit program\n");

        if(isNaN(toDo))
        {
            //incorrect input
            console.log("Unknown input");
        }
        else
        {
            if (toDo >2|| toDo< 1)
            {
                //incorrect input
                console.log("Unknown input")
                looping = 1;
            }
            else if (toDo == '1')
            {
                //start conversion process from checking currency
                currencyPresent();
                looping = 1;
            }
            else
            {
                console.log("Have a nice day!");
                looping = 0;
                break;
            }
        }
    }
}

//greet user, explain program
function main()
{
    displayRates();
    whatDoYouWantToDo();

}

//Test to see if currency is correct
function currencyPresent()
{
    console.log("What do you want to convert?");
    let currencyFrom = input("From: ").toUpperCase();
    if(rateMap.has(currencyFrom))
    {
        let currencyTo = input("To: ").toUpperCase();
        if(rateMap.has(currencyTo))
        {
            let amount = input("Amount: ");
            amountChecks( amount, currencyFrom, currencyTo);
        }
        else
        {
            console.log("Unknown currency");
            currencyPresent();
        }
    }
    else
    {
        console.log("Unknown currency");
        currencyPresent();
    }
}

//Function to perform checks on the amount
function amountChecks(amount, currencyFrom, currencyTo)
{
    if(isNaN(Number(amount)))
    {
        console.log("The amount has to be a number");
    }
    else if (amount < 1)
    {
        console.log("The amount cannot be less than 1");
    }
    //Perform conversion if the amount is a number > 1
    else
        performConversion(amount, currencyFrom, currencyTo);

}

//Performs conversion on demand
function performConversion(amount, currencyFrom, currencyTo)
{
    let fromRate = rateMap.get(currencyFrom);
    let toRate = rateMap.get(currencyTo);
    let finalAmount = amount * toRate / fromRate;

    console.log("Result: "+ amount +" "+ currencyFrom +" equals " + finalAmount.toFixed(4) + " " + currencyTo);
    /*
    let finalAmount = rateMap.get(currencyTo) * amount;
    console.log("Result: "+ amount + " USD equals " + finalAmount.toFixed(4) + " " + currencyTo);
    */
}

main();