<template>
  <div>
    <div id="map"></div>
  </div>
</template>

<script>
import { Scene, PointLayer, Popup } from "@antv/l7";
import { GaodeMap } from "@antv/l7-maps";

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

    fetch("https://gw.alipayobjects.com/os/basement_prod/9078fd36-ce8d-4ee2-91bc-605db8315fdf.csv")
      .then(res => res.text())
      .then(data => {
        const pointLayer = new PointLayer({})
          .source(data, {
            parser: {
              type: "csv",
              x: "Longitude",
              y: "Latitude"
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
            .setHTML(`<span>车次: ${e.feature.info}</span>`);
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
