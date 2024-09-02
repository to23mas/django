import { Network, DataSet } from 'vis-network/standalone/esm/vis-network';

export function initVisNetwork() {
	document.addEventListener('DOMContentLoaded', () => {
		const container = document.getElementById('network');

		const parsedNodes = window.graphData.nodes;
		const parsedEdges = window.graphData.edges;

		const nodes = new DataSet(parsedNodes);
		const edges = new DataSet(parsedEdges);

		const options = {};
		const network = new Network(
			document.getElementById("projectNetwork"),
			{nodes: nodes, edges: edges},
			{
				edges: {
					color: { color: '#cccccc' },
					chosen: false,
				},
				nodes: {
					font: {
						size: 20
					},
					fixed: {
						x: true,
						y: true
					},
					shape: 'ellipse'
				},
				layout: {
					randomSeed: 2
				},
			}
		);

		network.on("selectNode", function (params) {
			if (params.nodes.length === 1) {
				var node = nodes.get(params.nodes[0]);
				if (node.url !== '#') {
					window.location.href = node.url;
				}
		}});

		const originalColors = new Map(parsedNodes.map(node => [node.id, node.color]));
		network.on('click', function (params) {
			if (params.nodes.length > 0) {
				const selectedNodeId = params.nodes[0];
				const connectedNodes = network.getConnectedNodes(selectedNodeId);
				const allNodes = nodes.get();

				nodes.update(allNodes.map(node => {
					if (connectedNodes.includes(node.id) || node.id === selectedNodeId) {
						return { id: node.id, color: originalColors.get(node.id) };
					} else {
						return { id: node.id, color: { background: '#D3D3D3', border: '#A9A9A9' } };
					}
				}));
			} else {
				nodes.update(nodes.get().map(node => ({
					id: node.id,
					color: originalColors.get(node.id)
				})));
			}
		});
	});
}
