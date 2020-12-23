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
      colors.push('rgba(' + Charter.getSentimentColor(dataPoint.label) + ', 0.5)');
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
   * Creates a vertical bar chart.
   *
   * @param chardId
   *   The ID attribute of the canvas tag you want to turn into a chart.
   * @param dataSet
   *   An object of chart data.
   */
  'createVerticalBarChart': (chartId, data) => {
    data.datasets.forEach((v, i) => {
      let sm_color = Charter.getSocialMediaColor(data.datasets[i].social_media_source);
      data.datasets[i].backgroundColor = 'rgba(' + sm_color + ', 0.5)';
      data.datasets[i].borderColor = 'rgba(' + sm_color + ', 1)';
      data.datasets[i].borderWidth = 1;
    });
    new Chart(document.getElementById(chartId), {
      'type': 'bar',
      'data': data,
      'options': {}
    });
  },

  /**
   * Gets a color for a sentiment.
   *
   * @param sentiiment
   *   'positive', 'negative' or 'neutral'.
   *
   * @return string
   *   An RGB string like "255, 255, 255".
   */
  'getSentimentColor': (sentiment) => {
    if (sentiment.toLowerCase() == 'positive') {
      return '3, 84, 25';
    }
    else if (sentiment.toLowerCase() == 'negative') {
      return '138, 15, 0';
    }
    else if (sentiment.toLowerCase() == 'neutral') {
      return '166, 162, 41';
    }
    else {
      return '134, 92, 189';
    }
  },

  /**
   * Gets social media branding color.
   *
   * @param social_media_platform
   *   The name of a social media platform (e.g. 'Reddit').
   *
   * @return string
   *   An RGB string like "255, 255, 255".
   */
  'getSocialMediaColor': (social_media_platform) => {
    if (social_media_platform.toLowerCase() == 'reddit') {
      return '255, 69, 0'
    }
    else if (social_media_platform.toLowerCase() == 'twitter') {
      return '29, 161, 242';
    }
    else {
      return '240, 240, 240';
    }
  }
};
