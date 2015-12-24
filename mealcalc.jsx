(function (window) {
  window.React = require('react');
  window.ReactDOM = require('react-dom');
  window.agent = require('superagent');

  function calcStats(items) {
    var stats = {
      calories: 0,
      protein: 0,
      carbs: 0,
      fat: 0,
    };

    items.forEach(function (i) {
      stats.calories += i.calories;
      stats.protein += i.protein;
      stats.carbs += i.carbs;
      stats.fat += i.fat;
    });

    return stats;
  }

  function calcWidth(macro, calsg, totalCal) {
    return Math.round(macro * calsg * 100 / totalCal);
  }

  var PrettyNumber = React.createClass({
    render: function () {
      var parts = this.props.number.toFixed(1).split('.');

      return (
        <span>{parts[0]}.<small>{parts[1]}</small></span>
      );
    }
  });

  var Spacer = React.createClass({
    render: function () {
      var field = this.props.field;
      var number = this.props.stats[field];

      var width;
      var cals = this.props.stats.calories;

      // show remainder as fat to give 100% width..
      if (field === 'fat') {
        var p = this.props.stats.protein;
        var c = this.props.stats.carbs;

        width = 100 - calcWidth(p, 4, cals) - calcWidth(c, 4, cals);

      } else {
        width = calcWidth(number, 4, cals);
      }

      width = width.toFixed(1) + '%';

      return (
        <span className={'spacer spacer-' + field} style={{width: width}}>
          &nbsp;
        </span>
      );
    }
  });

  var Meal = React.createClass({
    render: function () {
      return (
        <div className="meal">
          <div className="clear">
            <p className="calories">
              <PrettyNumber number={this.props.stats.calories} /> cal
            </p>
            <p>{this.props.name}</p>
            <p className="stats">
              <PrettyNumber number={this.props.stats.protein} />g protein&nbsp;
              <PrettyNumber number={this.props.stats.carbs} />g carbs&nbsp;
              <PrettyNumber number={this.props.stats.fat} />g fat&nbsp;
            </p>
          </div>
          <div className="clear">
            <Spacer stats={this.props.stats} field={'protein'} />
            <Spacer stats={this.props.stats} field={'carbs'} />
            <Spacer stats={this.props.stats} field={'fat'} />
          </div>
        </div>
      );
    }
  });

  var CustomMealBox = React.createClass({
    getInitialState: function () {
      return {p: 0, c: 0, v: 0};
    },
    update: function (itemType) {
      var self = this;

      return function (val) {
        var obj = {};
        obj[itemType] = val;
        self.setState(obj);
      };
    },
    render: function () {
      var items = [
        this.props.proteins[this.state.p],
        this.props.carbs[this.state.c],
        this.props.veggies[this.state.v]
      ];

      var stats = calcStats(items);
      var name = items.map(function (i) { return i.name; }).join(' + ');

      return (
        <div>
          <CustomMealSelect
            items={this.props.proteins}
            index={this.state.p}
            update={this.update('p')} />

          <CustomMealSelect
            items={this.props.carbs}
            index={this.state.c}
            update={this.update('c')} />

          <CustomMealSelect
            items={this.props.veggies}
            index={this.state.v}
            update={this.update('v')} />

          <Meal stats={stats} name={name} />
        </div>
      );
    }
  });

  var CustomMealSelect = React.createClass({
    handleChange: function (e) {
      this.props.update(e.target.value);
    },
    render: function () {
      return (
        <select value={this.props.index} onChange={this.handleChange}>
          {
            this.props.items.map(function (item, i) {
              return (
                <option key={i} value={i}>{item.name}</option>
              );
            })
          }
        </select>
      );
    }
  });

  var MealList = React.createClass({
    render: function () {
      return (
        <ul>
          {
            this.props.meals.map(function (meal, i) {
              return (
                <li key={i}><Meal stats={meal} name={meal.name} /></li>
              );
            })
          }
        </ul>
      );
    }
  });

  var MealCalcApp = React.createClass({
    render: function () {
      return (
        <div className="clear">
          <div className="mc-panel">
            <CustomMealBox
              proteins={this.props.data.proteins}
              carbs={this.props.data.carbs}
              veggies={this.props.data.veggies} />
            <MealList meals={this.props.data.meals} />
          </div>
          <div className="mc-panel">
            <p>right panel</p>
            <p>right panel</p>
            <p>right panel</p>
            <p>right panel</p>
            <p>right panel</p>
            <p>right panel</p>
          </div>
        </div>
      );
    }
  });

  agent
    .get('/data')
    .end(function (err, result) {

      ReactDOM.render(
        <MealCalcApp data={result.body} />,
        document.getElementById('main-content')
      );
    });
})(window);
