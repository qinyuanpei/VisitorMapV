<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
import { Scene, PointLayer, Popup } from "@antv/l7";
import { GaodeMap } from "@antv/l7-maps";
import AV from "leancloud-storage";

export default {
  data() {
    return {
      scene: null,
      markerLayer: null
    };
  },
  mounted() {
    this.initMap();
    this.initAV();
    this.fetchData();
  },
  methods: {
    initMap: function() {
      this.scene = new Scene({
        id: "map",
        map: new GaodeMap({
          pitch: 0,
          style: "dark",
          center: [112, 23.69],
          zoom: 2.5
        })
      });
    },
    initAV: function() {
      AV.init({
        appId: "JbHqRp2eMrTgIwYpfERH0g79-gzGzoHsz",
        appKey: "VsiKvLuiBGvJL1XrAfv7siY2",
        serverURLs: "https://jbhqrp2e.lc-cn-n1-shared.com"
      });
    },
    drawLayer: function(data) {
      var self = this;
      if (self.markerLayer) {
        self.scene.removeLayer(self.markerLayer);
      }
      self.markerLayer = new PointLayer({})
        .source(data, {
          parser: {
            type: "json",
            x: "longitude",
            y: "latitude",
            total_pv: "total_pv",
            total_uv: "total_uv",
            city: "city"
          }
        })
        .shape("circle")
        .active(true)
        .animate(true)
        .size(56)
        .color("#4cfd47")
        .style({
          opacity: 1
        });
      self.markerLayer.on("mousemove", e => {
        const popup = new Popup({
          offsets: [0, 0],
          closeButton: false
        })
          .setLnglat(e.lngLat)
          .setHTML(
            `<span>${e.feature.city}</span><br/><span>${e.feature.total_uv}</span>个人来过，共<span>${e.feature.total_pv}</span>个足迹`
          );
        self.scene.addPopup(popup);
      });
      self.scene.addLayer(self.markerLayer);
    },
    fetchData: function() {
      var self = this;
      var query = new AV.Query("LocationSummary");
      query.limit(1000);
      query.find().then(data => {
        data = data.map(x => x._serverData);
        self.drawLayer(data);
      });
    }
  }
};
</script>

<style>
::-webkit-scrollbar {
  display: none;
}

html,
body {
  overflow: hidden;
  margin: 0;
}

#map {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 100%;
}
