(function (window) {
  window.React = require('react');
  window.agent = require('superagent');

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
      var p = this.props.proteins[this.state.p];
      var c = this.props.carbs[this.state.c];
      var v = this.props.veggies[this.state.v];

      var calories = p.calories + c.calories + v.calories;
      var protein = p.protein + c.protein + v.protein;
      var carbs = p.carbs + c.carbs + v.carbs;
      var fat = p.fat + c.fat + v.fat;

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

          <p>Total calories = {calories.toFixed(1)}</p>
          <p>Total protein = {protein.toFixed(1)}g</p>
          <p>Total carbs = {carbs.toFixed(1)}g</p>
          <p>Total fat = {fat.toFixed(1)}g</p>
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

      var proteins = result.body.proteins.map(convert);
      var carbs = result.body.carbs.map(convert);
      var veggies = result.body.veggies.map(convert);

      React.render(
        <CustomMealBox proteins={proteins} carbs={carbs} veggies={veggies} />,
        document.getElementById('main-content')
      );
    });
})(window);
