# Interactive Power Dynamics Visualizations
## Observable Notebook

This notebook provides interactive D3.js visualizations for exploring power dynamics in the debate transcript.

**To use this notebook:**
1. Import the data file `d3_visualization_data.json` into Observable
2. Copy the cells below into an Observable notebook
3. The visualizations will automatically update with your data

---

## Data Import

```javascript
data = FileAttachment("d3_visualization_data.json").json()
```

---

## 1. Interactive Network Graph

```javascript
{
  const width = 800;
  const height = 600;
  
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height);
  
  const simulation = d3.forceSimulation(data.network.nodes)
    .force("link", d3.forceLink(data.network.links).id(d => d.id).distance(100))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2));
  
  const link = svg.append("g")
    .selectAll("line")
    .data(data.network.links)
    .join("line")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.6)
    .attr("stroke-width", d => Math.sqrt(d.value) * 2);
  
  const node = svg.append("g")
    .selectAll("circle")
    .data(data.network.nodes)
    .join("circle")
    .attr("r", d => Math.sqrt(d.speaking_time) / 3)
    .attr("fill", "#69b3a2")
    .call(drag(simulation));
  
  const label = svg.append("g")
    .selectAll("text")
    .data(data.network.nodes)
    .join("text")
    .text(d => d.id)
    .attr("font-size", "10px")
    .attr("dx", d => Math.sqrt(d.speaking_time) / 3 + 5)
    .attr("dy", 4);
  
  simulation.on("tick", () => {
    link
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);
    
    node
      .attr("cx", d => d.x)
      .attr("cy", d => d.y);
    
    label
      .attr("x", d => d.x)
      .attr("y", d => d.y);
  });
  
  function drag(simulation) {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }
    
    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }
    
    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }
    
    return d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended);
  }
  
  return svg.node();
}
```

---

## 2. Interactive Timeline

```javascript
{
  const width = 1000;
  const height = 400;
  const margin = {top: 20, right: 20, bottom: 40, left: 100};
  
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height);
  
  const x = d3.scaleLinear()
    .domain([0, data.metadata.meeting_duration])
    .range([margin.left, width - margin.right]);
  
  const speakers = [...new Set(data.timeline.map(d => d.speaker))].slice(0, 10);
  const y = d3.scaleBand()
    .domain(speakers)
    .range([margin.top, height - margin.bottom])
    .padding(0.1);
  
  const color = d3.scaleOrdinal(d3.schemeCategory20);
  
  const bars = svg.append("g")
    .selectAll("rect")
    .data(data.timeline.filter(d => speakers.includes(d.speaker)))
    .join("rect")
    .attr("x", d => x(d.start))
    .attr("y", d => y(d.speaker))
    .attr("width", d => x(d.end) - x(d.start))
    .attr("height", y.bandwidth())
    .attr("fill", d => color(d.speaker))
    .attr("opacity", 0.7)
    .on("mouseover", function(event, d) {
      d3.select(this).attr("opacity", 1);
      tooltip.style("visibility", "visible")
        .html(`${d.speaker}<br>${d.start.toFixed(1)}s - ${d.end.toFixed(1)}s<br>${d.duration.toFixed(1)}s`);
    })
    .on("mousemove", function(event) {
      tooltip.style("top", (event.pageY - 10) + "px")
        .style("left", (event.pageX + 10) + "px");
    })
    .on("mouseout", function() {
      d3.select(this).attr("opacity", 0.7);
      tooltip.style("visibility", "hidden");
    });
  
  const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("background", "rgba(0,0,0,0.8)")
    .style("color", "white")
    .style("padding", "5px")
    .style("border-radius", "3px")
    .style("visibility", "hidden");
  
  svg.append("g")
    .attr("transform", `translate(0,${margin.top})`)
    .call(d3.axisLeft(y));
  
  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickFormat(d => `${(d/60).toFixed(1)}m`));
  
  return svg.node();
}
```

---

## 3. Interactive Heatmap

```javascript
{
  const width = 1000;
  const height = 600;
  const margin = {top: 100, right: 50, bottom: 50, left: 150};
  
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height);
  
  const speakers = data.participation_heatmap.data.map(d => d.speaker);
  const segments = data.participation_heatmap.n_segments;
  
  const x = d3.scaleBand()
    .domain(d3.range(segments))
    .range([margin.left, width - margin.right])
    .padding(0.05);
  
  const y = d3.scaleBand()
    .domain(speakers)
    .range([margin.top, height - margin.bottom])
    .padding(0.05);
  
  const maxTime = d3.max(data.participation_heatmap.data, d => 
    d3.max(d.segments, s => s.time));
  
  const color = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, maxTime]);
  
  const cells = svg.append("g")
    .selectAll("rect")
    .data(data.participation_heatmap.data.flatMap(d => 
      d.segments.map(s => ({speaker: d.speaker, segment: s.segment, time: s.time}))
    ))
    .join("rect")
    .attr("x", d => x(d.segment))
    .attr("y", d => y(d.speaker))
    .attr("width", x.bandwidth())
    .attr("height", y.bandwidth())
    .attr("fill", d => color(d.time))
    .attr("stroke", "#fff")
    .attr("stroke-width", 0.5)
    .on("mouseover", function(event, d) {
      d3.select(this).attr("stroke-width", 2);
      tooltip.style("visibility", "visible")
        .html(`${d.speaker}<br>Segment ${d.segment + 1}<br>${d.time.toFixed(1)}s`);
    })
    .on("mousemove", function(event) {
      tooltip.style("top", (event.pageY - 10) + "px")
        .style("left", (event.pageX + 10) + "px");
    })
    .on("mouseout", function() {
      d3.select(this).attr("stroke-width", 0.5);
      tooltip.style("visibility", "hidden");
    });
  
  const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("position", "absolute")
    .style("background", "rgba(0,0,0,0.8)")
    .style("color", "white")
    .style("padding", "5px")
    .style("border-radius", "3px")
    .style("visibility", "hidden");
  
  svg.append("g")
    .attr("transform", `translate(0,${margin.top})`)
    .call(d3.axisLeft(y));
  
  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisTop(x).tickFormat(d => d + 1));
  
  return svg.node();
}
```

---

## 4. Interactive Lorenz Curve

```javascript
{
  const width = 600;
  const height = 600;
  const margin = {top: 20, right: 20, bottom: 60, left: 60};
  
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height);
  
  const x = d3.scaleLinear()
    .domain([0, 1])
    .range([margin.left, width - margin.right]);
  
  const y = d3.scaleLinear()
    .domain([0, 1])
    .range([height - margin.bottom, margin.top]);
  
  const line = d3.line()
    .x(d => x(d.cumulative_speakers))
    .y(d => y(d.cumulative_time))
    .curve(d3.curveMonotoneX);
  
  const equalityLine = d3.line()
    .x(d => x(d.cumulative_speakers))
    .y(d => y(d.perfect_equality))
    .curve(d3.curveLinear);
  
  // Area between curves
  const area = d3.area()
    .x(d => x(d.cumulative_speakers))
    .y0(d => y(d.perfect_equality))
    .y1(d => y(d.cumulative_time))
    .curve(d3.curveMonotoneX);
  
  svg.append("path")
    .datum(data.lorenz_curve)
    .attr("fill", "rgba(0,0,0,0.2)")
    .attr("d", area);
  
  svg.append("path")
    .datum(data.lorenz_curve)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line);
  
  svg.append("path")
    .datum(data.lorenz_curve)
    .attr("fill", "none")
    .attr("stroke", "red")
    .attr("stroke-width", 2)
    .attr("stroke-dasharray", "5,5")
    .attr("d", equalityLine);
  
  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickFormat(d3.format(".0%")));
  
  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y).tickFormat(d3.format(".0%")));
  
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", height - 10)
    .attr("text-anchor", "middle")
    .text("Cumulative Proportion of Speakers");
  
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 15)
    .attr("x", -height / 2)
    .attr("text-anchor", "middle")
    .text("Cumulative Proportion of Speaking Time");
  
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", margin.top)
    .attr("text-anchor", "middle")
    .attr("font-size", "16px")
    .text(`Gini Coefficient: ${Math.abs(data.inequality_metrics.gini_coefficient).toFixed(3)}`);
  
  return svg.node();
}
```

---

## 5. Speaker Filter Controls

```javascript
viewof selectedSpeakers = {
  const form = html`<form>
    <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px;">
      ${Object.keys(data.speaker_times).map(speaker => html`
        <label style="display: flex; align-items: center; gap: 5px;">
          <input type="checkbox" value="${speaker}" checked>
          <span>${speaker}</span>
        </label>
      `)}
    </div>
  </form>`;
  
  form.addEventListener("change", () => {
    form.value = Array.from(form.querySelectorAll("input:checked")).map(i => i.value);
    form.dispatchEvent(new CustomEvent("input"));
  });
  
  form.value = Object.keys(data.speaker_times);
  return form;
}
```

---

## Usage Instructions

1. **Import Data**: Upload `d3_visualization_data.json` to Observable
2. **Copy Cells**: Copy each visualization cell into your Observable notebook
3. **Interact**: Hover over elements to see details, drag network nodes, filter speakers
4. **Customize**: Modify colors, sizes, and interactions as needed

---

## Standalone HTML Version

A standalone HTML file (`interactive_visualizations.html`) is also provided for use without Observable.
