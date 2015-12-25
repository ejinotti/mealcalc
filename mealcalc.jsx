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
      var classes = 'meal';

      if (!this.props.click) {
        classes += ' total';
      }

      return (
        <div className={classes} onClick={this.props.click}>
          <div className="clear">
            <p className="calories">
              <PrettyNumber number={this.props.meal.calories} /> cal
            </p>
            <p>{this.props.meal.name}</p>
            <p className="stats">
              <PrettyNumber number={this.props.meal.protein} />g protein&nbsp;
              <PrettyNumber number={this.props.meal.carbs} />g carbs&nbsp;
              <PrettyNumber number={this.props.meal.fat} />g fat&nbsp;
            </p>
          </div>
          <div className="clear">
            <Spacer stats={this.props.meal} field={'protein'} />
            <Spacer stats={this.props.meal} field={'carbs'} />
            <Spacer stats={this.props.meal} field={'fat'} />
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

      var meal = calcStats(items);
      meal.name = items.map(function (i) { return i.name; }).join(' + ');

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

          <Meal meal={meal} click={this.props.clickfn(meal)} />
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
      var self = this;

      return (
        <ul>
          {
            this.props.meals.map(function (meal, i) {
              return (
                <li key={i}>
                  <Meal
                    meal={meal}
                    click={self.props.clickfn(meal, i)} />
                </li>
              );
            })
          }
        </ul>
      );
    }
  });

  var MealCalcApp = React.createClass({
    getInitialState: function () {
      return {selectedMeals: []};
    },
    addMeal: function (meal, i) {
      return function () {
        var meals = this.state.selectedMeals;
        meals.push(meal);
        this.setState({selectedMeals: meals});
      }.bind(this);
    },
    removeMeal: function (meal, i) {
      return function () {
        var meals = this.state.selectedMeals;
        meals.splice(i, 1);
        this.setState({selectedMeals: meals});
      }.bind(this);
    },
    clear: function () {
      this.setState({selectedMeals: []});
    },
    render: function () {
      var list = this.props.data.meals.concat(this.props.data.breakfasts);
      var selected = this.state.selectedMeals;
      var total = '';

      if (selected.length) {
        var meal = calcStats(selected);
        meal.name = 'TOTAL';
        total = (
          <div id="total-display">
            <Meal meal={meal} />
            <button onClick={this.clear}>CLEAR ALL</button>
          </div>
        );
      }

      return (
        <div className="clear">
          <div className="mc-panel">
            <CustomMealBox
              proteins={this.props.data.proteins}
              carbs={this.props.data.carbs}
              veggies={this.props.data.veggies}
              clickfn={this.addMeal} />
            <MealList
              meals={list}
              clickfn={this.addMeal} />
          </div>
          <div className="mc-panel">
            {total}
            <MealList
              meals={this.state.selectedMeals}
              clickfn={this.removeMeal} />
          </div>
        </div>
      );
    }
  });

  agent
    .get('/data')
    .end(function (err, result) {
      console.log(result.body);

      ReactDOM.render(
        <MealCalcApp data={result.body} />,
        document.getElementById('main-content')
      );
    });
})(window);
