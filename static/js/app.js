
function buildChartsPlottable(team) {

  //set chart dimensions
  var chartWidth = 960;
  var chartHeight = 620;

  //select chart and clear html
  var chart1 = d3.select("#chart-1").html("");

  //append a div to hold actual chart
  var svg1 = chart1.append("div")
    .attr("id", "c1")
    .style('width', chartWidth + "px")
    .style('height', chartHeight + "px");

  //save url
  var url1 = "/teams/winpct"

  //begin function with accessing history of all teams
  d3.json(url1).then(function(data) {

    console.log(data);
    //create a plottable dataset
    var allData = data;
    console.log(allData);
    var dataset = new Plottable.Dataset(allData);

    //create scales, axes, and labels
    var xScale = new Plottable.Scales.Linear();
    var yScale = new Plottable.Scales.Linear();
    var xAxis = new Plottable.Axes.Numeric(xScale, "bottom");
    var yAxis = new Plottable.Axes.Numeric(yScale, "left");
    var xLabel = new Plottable.Components.AxisLabel("Year", 0);
    var yLabel = new Plottable.Components.AxisLabel("Win Percentage", 270);

    //functions to get variables
    var projectYear = function(d) {return +d.Year;};
    var projectWinPrct = function(d) {return +d.WinPrct};

    //set up a dataset for the individual team and get the data
    var teamData = [];
    allData.forEach(d => {
      //push if team in question
      if (d.FranchiseID == team) {
        teamData.push(d);
      }
    });
    var teamSet = new Plottable.Dataset(teamData);

    console.log(teamData);

    //create title
    var title = new Plottable.Components.TitleLabel(team + " Team Performance", 0)
      .yAlignment("top");

    //make a scatter plot of all performances
    var allScatter = new Plottable.Plots.Scatter();
    allScatter.addDataset(dataset);
    allScatter.x(projectYear, xScale)
              .y(projectWinPrct, yScale)
              .attr("fill", "gray")
              .attr("opacity", .5);

    //make a line plot of the team's historic performance
    var teamLine = new Plottable.Plots.Line();
    teamLine.addDataset(teamSet);
    teamLine.x(projectYear, xScale)
            .y(projectWinPrct, yScale)
            .attr("stroke", function(d) {return d.Color1});

    //construct graph
    var plots = new Plottable.Components.Group([allScatter, teamLine, title]);
    var table = new Plottable.Components.Table([
      [yLabel, yAxis, plots],
      [null, null, xAxis],
      [null, null, xLabel]
    ]);

    //render graph
    table.renderTo("div#c1");



    
  });
}

/* function buildBestHitterChart(teams, batstat)
{

  var url = `/batting/${teams}/${batstat}`;
  d3.json(url).then(function(data){
  var PlayerName = data.PlayerName;
  var BatStat = data.Stat;

    
    var trace1 = {
      type: 'scatter',
      x: PlayerName,
      y: BatStat,
      mode: 'markers',
      marker: {
        color: data.Color1,
        line: {
          color: data.Color1,
          width: 1,
        },
        symbol: 'circle',
        size: 16
      }
    };
    
    var data = [trace1];

  var layout = {
    title: `${teams} Top 10 Best ${batstat} of All Time`,
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
    width: 900,
    height: 700,
    paper_bgcolor: 'rgb(254, 247, 234)',
    plot_bgcolor: 'rgb(254, 247, 234)',
    hovermode: 'closest'
  };

  Plotly.newPlot('chart-2', data, layout);
  
  });
}; */

//function to build top ten hitters chart
function buildHittingChart(teams, batstat){
  
  //get url
  var url = `/batting/${teams}/${batstat}`;

  //get data
  d3.json(url).then(function(data){

    //save data
    var PlayerName = data.PlayerName;
    var BatStat = data.Stat;

    //create data object
    var d = [{
      type: 'bar',
      x: PlayerName,
      y: BatStat,
      marker: {color: data.Color1}
    }];

    //create layout
    var layout = {title: `${teams} Top 10 ${batstat} of All Time`,
      showlegend: false,
    };

    //create graph
    Plotly.newPlot('chart-2', d, layout);
  });
}

//function to build top ten pitchers chart
function buildPitchingChart(teams, pitchstat) 
{
  //save url
  var url = `/pitching/${teams}/${pitchstat}`;

  //get data
  d3.json(url).then(function(data){
    //save data
    var PlayerName = data.PlayerName;
    var PitchStat = data.Stat;
    
    //create data object
    var d = [{
      type: 'bar',
      y: PitchStat,
      x: PlayerName,
      //orientation: 'h',
      marker: {color: data.Color1}
    }];

    //create layout
    var layout = {title: `${teams} Top 10 ${pitchstat} of All Time`,
      showlegend: false,
      //width : 1250
    };
    
    //create graph
    Plotly.newPlot('chart-3', d, layout);
  });

}

//teams available
names = ["ANA"
    ,"ARI"
    , "ATL"
    ,"BAL"
    ,'BOS'
    ,'CHC'
    ,'CHW'
    ,'CIN'
    ,'CLE'
    ,'COL'
    ,'DET'
    ,"FLA"
    ,'HOU'
    ,"KCR"
    ,"LAD"
    ,"MIL"
    ,"MIN"
    ,"NYM"
    ,"NYY"
    ,"OAK"
    ,"PHI"
    ,"PIT"
    ,"SDP"
    ,"SEA"
    ,"SFG"
    ,"STL"
    ,"TBD"
    ,"TEX"
    ,"TOR"
    ,"WSN"];

//available batting stats
batStats = ['HR', 'H', '1B', '2B', '3B', 'AB', 'K', 'G', 'BB', 'SF', 'HBP',
  'AVG', 'OBP', 'SLG', 'OPS'];

//available pitching stats
pitchStats = ['ERA', 'IP', 'G', 'GS', 'ER', 'SV', 'SHO', 'CG', 'BB', 
'K', 'BB_Rate', 'HR_Rate'];

//function to start page
function init() {

  //grab references to the selectors
  var teamSelect = d3.select("#selTeam");
  var batSelect = d3.select("#selBatStat");
  var pitchSelect = d3.select("#selPitchStat");

  //populate the team names
  names.forEach((team) => {
    teamSelect.append("option").text(team).property("value", team);
  });

  //populate the batting stats
  batStats.forEach((stat) => {
    batSelect.append("option").text(stat).property("value", stat);
  });

  //populate the pitching stats
  pitchStats.forEach((stat) => {
    pitchSelect.append("option").text(stat).property("value", stat);
  });

  //grab the first team
  var firstTeam = names[0];

  //set team value
  teamSelect.property("value", firstTeam);

  //choose some beginning stats
  var firstBatStat = batStats[0];
  var firstPitchStat = pitchStats[0];

  //build first charts
  window.setTimeout(buildChartsPlottable(firstTeam), 30000);
  window.setTimeout(buildHittingChart(firstTeam, firstBatStat), 60000);
  window.setTimeout(buildPitchingChart(firstTeam, firstPitchStat), 90000);

}

//function to handle team selection
function teamChanged(team) {

  //grab first stats
  var firstBatStat = batStats[0];
  var firstPitchStat = pitchStats[0];

  //set team value
  d3.select("#selTeam").property("value", team);

  //build new charts
  window.setTimeout(buildChartsPlottable(team), 30000);
  window.setTimeout(buildHittingChart(team, firstBatStat), 60000);
  window.setTimeout(buildPitchingChart(team, firstPitchStat), 90000);
}

//function to handle batting stat selection
function batChanged(bat_stat) {

  //get team
  var team = d3.select("#selTeam").property("value");

  console.log(team);

  //build new chart
  buildHittingChart(team, bat_stat);
}

//function to handle pitching stat selection
function pitchChanged(pitch_stat) {

  //get team
  var team = d3.select("#selTeam").property("value");

  //build new chart
  buildPitchingChart(team, pitch_stat);
}

//initialize the dashboard
init();