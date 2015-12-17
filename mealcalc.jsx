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
        <span>
          {parts[0]}.<small>{parts[1]}</small>
        </span>
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
      var stats = calcStats([
        this.props.proteins[this.state.p],
        this.props.carbs[this.state.c],
        this.props.veggies[this.state.v]
      ]);

      return (
        <div>
          <CustomMealSelect items={this.props.proteins}
                            index={this.state.p}
                            update={this.update('p')} />

          <CustomMealSelect items={this.props.carbs}
                            index={this.state.c}
                            update={this.update('c')} />

          <CustomMealSelect items={this.props.veggies}
                            index={this.state.v}
                            update={this.update('v')} />

          <p>
            <PrettyNumber n={stats.protein} />g-protein&nbsp;
            <PrettyNumber n={stats.carbs} />g-carbs&nbsp;
            <PrettyNumber n={stats.fat} />g-fat&nbsp;
            (<PrettyNumber n={stats.calories} /> cals)
          </p>
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

  // var MealList = React.createClass({
  //
  // });
  //
  // var Meal = React.createClass({
  //
  // });

  var MealCalcApp = React.createClass({
    render: function () {
      return (
        <CustomMealBox proteins={this.props.data.proteins}
                       carbs={this.props.data.carbs}
                       veggies={this.props.data.veggies} />
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
