//
// This file auto-generated with generate-wrappers.js
//

var _ = require('underscore');
var THREE = require('three');
var widgets = require('@jupyter-widgets/base');
var dataserializers = require('jupyter-dataserializers');

var LightModel = require('./Light.autogen.js').LightModel;


var RectAreaLightModel = LightModel.extend({

    defaults: function() {
        return _.extend(LightModel.prototype.defaults.call(this), {

            type: "RectAreaLight",

        });
    },

    constructThreeObject: function() {

        var result = new THREE.RectAreaLight();
        return Promise.resolve(result);

    },

    createPropertiesArrays: function() {

        LightModel.prototype.createPropertiesArrays.call(this);

        this.props_created_by_three['type'] = true;
        this.props_created_by_three['rotation'] = true;
        this.props_created_by_three['quaternion'] = true;
        this.props_created_by_three['matrixWorldNeedsUpdate'] = true;

        this.property_converters['type'] = null;


    },

}, {

    model_name: 'RectAreaLightModel',

    serializers: _.extend({
    },  LightModel.serializers),
});

module.exports = {
    RectAreaLightModel: RectAreaLightModel,
};
