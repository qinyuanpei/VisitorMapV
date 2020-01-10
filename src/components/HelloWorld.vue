<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
import { Scene, PointLayer, Popup } from "@antv/l7";
import { GaodeMap } from "@antv/l7-maps";
import AV from "leancloud-storage"

export default {
  data() {
    return {};
  },
  mounted() {
    const scene = new Scene({
      id: "map",
      map: new GaodeMap({
        pitch: 0,
        style: "dark",
        center: [112, 23.69],
        zoom: 2.5
      })
    });
    
    AV.init({appId: "JbHqRp2eMrTgIwYpfERH0g79-gzGzoHsz", appKey: "VsiKvLuiBGvJL1XrAfv7siY2", serverURLs: "https://jbhqrp2e.lc-cn-n1-shared.com"});
    var query = new AV.Query('LocationSummary');
    query.limit(1000);
    query.find()
      .then(data => {
        const pointLayer = new PointLayer({})
          .source(JSON.stringify(data), {
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

        pointLayer.on("mousemove", e => {
          const popup = new Popup({
            offsets: [0, 0],
            closeButton: false
          })
            .setLnglat(e.lngLat)
            .setHTML(`<span>${e.feature.city}/${e.feature.total_pv}/${e.feature.total_uv}/</span>`);
          scene.addPopup(popup);
        });

        scene.addLayer(pointLayer);
      });
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
