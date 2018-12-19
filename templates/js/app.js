
function buildWinPctCharts(team) {
    
    // Connect to flask
    var url = "/teams/winpct";
    var location = get.getElementById('col1');
    d3.json(url).then(function(data) {
  
      // initiate data variables
      var xValues = data.FranchiseName;
      var yValues = data.WinPrct;
      var tValues = data.FranchiseName;
      var sizes = data.W;
      // var colors (need team colors)
      // Create Bubble Chart
      var trace_bubble = {
        x: xValues,
        y: yValues,
        text: tValues,
        mode: 'markers',
        marker: {
          size: sizes,
        }
      };
  
      var data = [trace_bubble];
  
      var layout = {
        xaxis: {title: "Teams Overall Wins and Win Percentage"}
      };
  
      Plotly.newPlot(location, data, layout);
  
      // Bar Graph Using Plotly
      url2 = "/teams/${team}"
      location2 = document.getElementById('col2');
      d3.json(url2).then(function(data) {
        // set variables
        var xValues = data.Year;
        var yValues = data.WinPrct;
        var WinWS = data.WinWS;
        var WinLeague = data.WinLeague;
        var WinDiv = data.WinDiv;
        var W = data.W;
        var L = data.L;
        var Division = data.Division;
        var League = data.League;
        var FranchiseName = data.FranchiseName;
        //var color ? (need access to team colors from SQL)
        // initiate data
        var data = [{
          x: xValues,
          y: yValues,
          type: 'bar',
          text:["Win World Series: " + WinWS,
                "Win " + Division + ": "  + WinDiv,
                "Win " + League + ": " + WinLeague,
                "Wins: " + W,
                "Losses: " + L,
                "Win Percentage: " +  WinPrct]

        }];
        // initiate layout
        var layout = {title: "Win Percentage to Year for: " + data.FranchiseName,
                      showlegend: false,
                      xaxis: {tickangle: -90},
                      bargap: 0.05
        };
  
        Plotly.newPlot(location2, data, layout);
      
      });
    });
  };
  

  
function buildBestHitterChart(team, bat_stat)
{
  var url = "/batting/${team}/${bat_stat}";

  var location = document.getElementById('col3');
  d3.json(url).then(function(data){
    var PlayerName = data.Player;
    var BatStat = data.bat_stat;

    
    var trace1 = {
      type: 'scatter',
      x: BatStat,
      y: PlayerName,
      mode: 'markers',
      name: 'Top 10 ' + bat_stat + " in " + team + " History!",
      marker: {
        color: 'rgba(156, 165, 196, 0.95)',
        line: {
          color: 'rgba(156, 165, 196, 1.0)',
          width: 1,
        },
        symbol: 'circle',
        size: 16
      }
    };
    
    var data = [trace1];

  var layout = {
    title: team + ' Best ' + bat_stat + 'of All Time!',
    xaxis: {
      showgrid: false,
      showline: true,
      linecolor: 'rgb(102, 102, 102)',
      titlefont: {
        font: {
          color: 'rgb(204, 204, 204)'
        }
      },
      tickfont: {
        font: {
          color: 'rgb(102, 102, 102)'
        }
      },
      autotick: false,
      dtick: 10,
      ticks: 'outside',
      tickcolor: 'rgb(102, 102, 102)'
    },
    margin: {
      l: 140,
      r: 40,
      b: 50,
      t: 80
    },
    legend: {
      font: {
        size: 10,
      },
      yanchor: 'middle',
      xanchor: 'right'
    },
    width: 600,
    height: 600,
    paper_bgcolor: 'rgb(254, 247, 234)',
    plot_bgcolor: 'rgb(254, 247, 234)',
    hovermode: 'closest'
  };

  Plotly.newPlot(location, data, layout);
  
  });
  
  

};