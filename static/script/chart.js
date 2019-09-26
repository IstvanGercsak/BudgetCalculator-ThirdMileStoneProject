// Collect data with each command and put it in a array from the color-by-value class
expense_value = [];
group_name = [];
background_color_array = [];
background_color_array_year = [];
year_month_array = [];


$(".get-number").each(function () {
    expense_value.push($(this).text());
});

$(".group_name").each(function (index_group_name) {
    group_name.push($(this).text());
    background_color_array[index_group_name] = getRandomColor();
});

$(".year-month").each(function (index_year_month) {
    year_month_array.push($(this).text());
    background_color_array_year[index_year_month] = getRandomColor();
});

function getRandomColor() {
    let letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

var bills = 0;
var savings = 0;
var income = 0;
var other = 0;
var shopping = 0;
var sumbalance;

sumbalance = $(".sum-balance").text();

if (sumbalance <= 0) {
    sumbalance = 0;
}

// equalize the goup sizes

for (j = group_name.length; group_name.length > expense_value.length; j--) {
    group_name.shift();
    console.log(group_name.length)
}

// Fill up Groups


if (group_name.length === expense_value.length) {

    for (var i = 0; i < group_name.length; i++) {
        if (group_name[i] === "Bills") {
            bills = bills + parseInt(expense_value[i]);
        } else if (group_name[i] === "Savings") {
            savings = savings + parseInt(expense_value[i]);
        } else if (group_name[i] === "Income") {
            income = income + parseInt(expense_value[i]);
        } else if (group_name[i] === "Other") {
            other = other + parseInt(expense_value[i]);
        } else if (group_name[i] === "Shopping") {
            shopping = shopping + parseInt(expense_value[i]);
        }
    }

}


var result = [
    ["Bills", "Savings", "Other", "Shopping", "Available money"],
    [bills, savings, other, shopping, sumbalance]
];

if (group_name.length > 0) {
    new Chart(document.getElementById("pie-chart"), {
        type: 'pie',
        data: {
            display: true,
            labels: result[0],
            datasets: [{
                label: "Budget Pie Chart",
                data: result[1],
                backgroundColor: background_color_array,
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Ratio of the expenses',
                fontColor: "#ffffff"
            },
            legend: {
                labels: {
                    fontColor: "#ffffff"
                },
            }
        }
    });
}
