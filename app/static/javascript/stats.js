var DAYS_IN_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
var HOURS_IN_DAY = ["00:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00",
                    "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

var username = [];
var msgQuantity = [];

for (i = 0; i < userActivity.length; i++) {
  username.push(userActivity[i][1]);
  msgQuantity.push(userActivity[i][2]);
}

Chart.defaults.global.legend.display = false;

var ctx = document.getElementById('mostActiveUsersBar').getContext('2d');

var mostActiveUsersChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: username,
        datasets: [{
            backgroundColor: 'rgb(108, 192, 145)',
            borderColor: 'rgb(108, 192, 145)',
            data: msgQuantity
        }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
      }
    }
});

Chart.defaults.global.legend.display = true;

var ctx1 = document.getElementById('top5Users').getContext('2d');

var top5UsersChart = new Chart(ctx1, {
    type: 'pie',
    data: {
        labels: username.slice(0, 5),
        datasets: [{
            backgroundColor: [
              'red',
              'blue',
              'green',
              'yellow',
              'orange'
            ],
            data: msgQuantity.slice(0, 5),
            label: 'label1'
        }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
});

Chart.defaults.global.legend.display = false;

var ctx2 = document.getElementById('statByDaysOfTheWeek').getContext('2d');

var statByDaysOfTheWeekChart = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: DAYS_IN_WEEK,
        datasets: [{
            backgroundColor: 'rgb(108, 192, 145)',
            borderColor: 'rgb(108, 192, 145)',
            data: timeStats[1],
            fill: false
        }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
      }
    }
});

var ctx3 = document.getElementById('statByHours').getContext('2d');

var statByHoursChart = new Chart(ctx3, {
    type: 'line',
    data: {
        labels: HOURS_IN_DAY,
        datasets: [{
            backgroundColor: 'rgb(108, 192, 145)',
            borderColor: 'rgb(108, 192, 145)',
            data: timeStats[0]
        }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
      }
    }
});
