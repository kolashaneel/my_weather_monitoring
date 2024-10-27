/*
 * Visualization source
 */
define([
            'jquery',
            'underscore',
            'api/SplunkVisualizationBase',
            'api/SplunkVisualizationUtils',
            'd3'
            // Add required assets to this list
        ],
        function(
            $,
            _,
            SplunkVisualizationBase,
            vizUtils,
            d3
        ) {
  
    // Extend from SplunkVisualizationBase
    return SplunkVisualizationBase.extend({
  
        initialize: function() {
            SplunkVisualizationBase.prototype.initialize.apply(this, arguments);
            this.$el = $(this.el);
            this.$el.addClass('single_value_viz');

            this.$el.append('<h3>This is a custom visualization stand in.</h3>');
            this.$el.append('<p>Edit your custom visualization app to render something here.</p>');
            
            // Initialization logic goes here
        },

        // Optionally implement to format data returned from search. 
        // The returned object will be passed to updateView as 'data'
        formatData: function(data) {

            // Format data
            console.log(data)
            if (data.rows.length < 1){
                return false
            }
            var datum = vizUtils.escapeHtml(data.rows[0][0])

            if(_.isNaN(datum)){
                throw new SplunkVisualizationBase.VisualizationError("this viz only supports number")
            }
            return datum;
        },
  
        // Implement updateView to render a visualization.
        //  'data' will be the data object returned from formatData or from the search
        //  'config' will be the configuration property object
        updateView: function(data, config) {
            
            // Draw something here
            if (!data){
                return ;
            }
            datum = data
            console.log(datum)
            this.$el.empty();
            height=220
            width=220
            var title = config[this.getPropertyNamespaceInfo().propertyNamespace + 'label'] || "Label";
            var unit = config[this.getPropertyNamespaceInfo().propertyNamespace + 'unit'] || "";
            var logo = config[this.getPropertyNamespaceInfo().propertyNamespace + 'logo'] || "default.png";
            var label_font_size = config[this.getPropertyNamespaceInfo().propertyNamespace + 'label_font_size'] || "29"
            var value_font_size = config[this.getPropertyNamespaceInfo().propertyNamespace + 'value_font_size'] || "70"
            var svg = d3.select(this.el).append('svg')
                .attr('class','svg-1')
                .attr('height',height)
                .attr('width',width)
                .attr('background','white')
            svg.append('image')
                .attr('class','svg-image')
                .attr('height','60')
                .attr('width','60')
                .attr('xlink:href','/static/app/my_weather_monitoring/images/'+logo)
            svg.append('text')
                .attr('class','svg_text')
                .attr('x',70)
                .attr('y',50)
                .text(title)
                .attr('font-size',label_font_size)
            svg.append('text')
                .attr('class','svg_value')
                .attr('x',100)
                .attr('y',140)
                .attr('text-anchor','middle')
                .text(datum+ " " +unit)
                .attr('font-size',value_font_size)
        },

        // Search data params
        getInitialDataParams: function() {
            return ({
                outputMode: SplunkVisualizationBase.ROW_MAJOR_OUTPUT_MODE,
                count: 10000
            });
        },

        // Override to respond to re-sizing events
        reflow: function() {}
    });
});