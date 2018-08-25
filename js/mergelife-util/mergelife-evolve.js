'use strict';var MergeLifeEvolve=function(a,b){this.zeros=function(a){for(var b=[],c=0;c<a[0];++c)b.push(1===a.length?0:this.zeros(a.slice(1)));return b},this.track=function(){var a=this.grid.rows,b=this.grid.cols,c=a*b;if(this.currentStats.mode===this.grid.gridMode){var j=this.currentStats.mage+1;this.currentStats.mage=j}else this.currentStats.mode=this.grid.gridMode,this.currentStats.mage=0;for(var d=0,e=0,f=0,g=0;g<this.grid.rows;g++)for(var k=0;k<this.grid.cols;k++){this.grid.mergeGrid[g][k]===this.grid.gridMode?(this.modeCount[g][k]++,this.lastModeStep[g][k]=this.grid.stepCount,50<this.modeCount[g][k]&&d++):this.modeCount[g][k]=0;var l=this.grid.stepCount-this.lastModeStep[g][k];25<this.grid.stepCount&&5<l&&25>l&&f++,this.lastColor[g][k]!==this.grid.mergeGrid[g][k]||this.grid.mergeGrid[g][k]===this.grid.gridMode?(this.lastColor[g][k]=this.grid.mergeGrid[g][k],this.lastColorCount[g][k]=0):(this.lastColorCount[g][k]++,5<this.lastColorCount[g][k]&&e++)}var h=c-(d+e+f),i=maximalRectangle(this.grid.mergeGrid,this.grid.gridMode);return this.currentStats.mc=d,this.currentStats.background=d/c,this.currentStats.foreground=e/c,this.currentStats.active=f/c,this.currentStats.chaos=h/c,this.currentStats.steps=this.grid.stepCount,this.currentStats.rect=i/c,this.currentStats},this.hasStabilized=function(){var a=this.currentStats.mc;if(a!==this.lastModeCount)this.modeCountSame=0,this.lastModeCount=a;else if(this.modeCountSame++,100<this.modeCountSame)return!0;return 1e3<this.grid.stepCount},this.objectiveFunctionCycle=function(a){for(var b=this;!this.hasStabilized();){this.grid.singleStep();var c=this.track();a&&console.log(JSON.stringify(c))}return this.objective.reduce(function(a,c){var d=c.max-c.min;c.stat in b.currentStats||console.log('Unknown objective stat: '+c.stat);var e=b.currentStats[c.stat];if(e<c.min)return a+c.min_weight;if(e>c.max)return a+c.max_weight;var f=(d/2-Math.abs(e-d/2))/(d/2);return f*=c.weight,a+f},0)},this.objective=b,this.grid=a,this.modeCount=this.zeros([this.grid.rows,this.grid.cols]),this.lastColor=this.zeros([this.grid.rows,this.grid.cols]),this.lastColorCount=this.zeros([this.grid.rows,this.grid.cols]),this.lastModeStep=this.zeros([this.grid.rows,this.grid.cols]),this.lastModeCount=0,this.modeCountSame=0,this.currentStats={},this.currentStats.mage=0,this.currentStats.mode=0,this.currentStats.mc=0,this.currentStats.background=0,this.currentStats.foreground=0,this.currentStats.active=0,this.currentStats.chaos=0};function maxAreaInHist(a){for(var b=[],c=0,d=0;c<a.length;)if(0===b.length||a[b[b.length-1]]<=a[c])b.push(c++);else{var e=b.pop();d=Math.max(d,a[e]*(0===b.length?c:c-b[b.length-1]-1))}return d}function maximalRectangle(a,b){for(var c=a.length,d=0===c?0:a[0].length,e=[],f=0,g=0;g<c;g++){e.push([]),e[g][d]=0;for(var h=0;h<d;h++)e[g][h]=a[g][h]===b?0===g?1:e[g-1][h]+1:0}for(var j,k=0;k<c;k++)j=maxAreaInHist(e[k]),j>f&&(f=j);return f}'undefined'!=typeof module&&'undefined'!=typeof module.exports&&(exports.MergeLifeEvolve=MergeLifeEvolve,exports.maximalRectangle=maximalRectangle);