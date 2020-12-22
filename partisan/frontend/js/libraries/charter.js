import '/static/node_modules/chart.js/dist/Chart.min.js';

/**
 * Class generator object.
 */
export const Charter = {

  /**
   * Builds a sentiment chart.
   *
   * @param chardId
   *   The ID attribute of the canvas tag you want to turn into a chart.
   * @param dataSet
   *   An array of data with elements of {label: value}.
   *   All values must sum to 100%.
   */
  'createSentimentPieChart': (chartId, dataSet) => {
    let labels = [];
    let values = [];
    let colors = [];
    let ctx = document.getElementById(chartId);
    dataSet.forEach((dataPoint) => {
      labels.push(dataPoint.label);
      values.push(dataPoint.value);
      colors.push(Charter.getColor(dataPoint.label));
    });
    new Chart(ctx, {
      'type': 'pie',
      'data': {
        'datasets': [{
          'data': values,
          'backgroundColor': colors
        }],
        'labels': labels
      },
      'options': {}
    })
  },

  /**
   * Gets a color for a sentiment.
   *
   * @param sentiiment
   *   'positive', 'negative' or 'neutral'.
   */
  'getColor': (sentiment) => {
    if (sentiment.toLowerCase() == 'positive') {
      return 'rgba(3, 84, 25, 0.5)';
    }
    else if (sentiment.toLowerCase() == 'negative') {
      return 'rgba(138, 15, 0, 0.5)';
    }
    else if (sentiment.toLowerCase() == 'neutral') {
      return 'rgba(166, 162, 41, 0.5)';
    }
    else {
      return 'rgba(134, 92, 189, 0.5)';
    }
  }
};
