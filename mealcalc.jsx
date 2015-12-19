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

  var PrettyNumber = React.createClass({
    render: function () {
      var parts = this.props.n.toFixed(1).split('.');
      return (
        <span>{parts[0]}.<small>{parts[1]}</small></span>
      );
    }
  });

  var Meal = React.createClass({
    render: function () {
      return (
        <div>
          <div>{this.props.name}</div>
          <PrettyNumber n={this.props.stats.protein} />g-protein&nbsp;
          <PrettyNumber n={this.props.stats.carbs} />g-carbs&nbsp;
          <PrettyNumber n={this.props.stats.fat} />g-fat&nbsp;
          (<PrettyNumber n={this.props.stats.calories} /> cals)
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
        <div>
          <div style={{width: '50%', float: 'left'}}>
            <CustomMealBox
              proteins={this.props.data.proteins}
              carbs={this.props.data.carbs}
              veggies={this.props.data.veggies} />
            <MealList meals={this.props.data.meals} />
          </div>
          <div>
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
      function convert(i) {
        return {
          name: i.name,
          calories: Number(i.calories),
          protein: Number(i.protein),
          carbs: Number(i.carbs),
          fat: Number(i.fat)
        };
      }

      var data = {};

      Object.keys(result.body).forEach(function (k) {
        data[k] = result.body[k].map(convert);
      });

      ReactDOM.render(
        <MealCalcApp data={data} />,
        document.getElementById('main-content')
      );
    });
})(window);
