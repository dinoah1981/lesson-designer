#!/usr/bin/env python3
"""
Generate HTML/JS Interactive Simulation from Competency

Creates self-contained HTML files with p5.js simulations when appropriate
for lesson competencies that involve interactive visualization.

Key features:
- Detects when simulation is appropriate based on competency keywords
- Pre-built p5.js sketches for common topics (economics, physics, biology)
- Self-contained HTML files (p5.js via CDN)
- Student instructions and keyboard controls
- Graceful handling when no simulation matches

Requirements covered:
    - MATL-04: Generate HTML/JS simulation programs when appropriate
"""

import os
import sys
from typing import Optional, Dict, List
from jinja2 import Template


# Simulation templates with p5.js sketches
SIMULATION_TEMPLATES = {
    'supply_demand': {
        'title': 'Supply and Demand Simulator',
        'learning_objective': 'Analyze how supply and demand curves interact to determine market equilibrium.',
        'instructions': 'Use the controls to shift the supply and demand curves. Observe how the equilibrium price and quantity change. Notice that when demand increases (curve shifts right), both price and quantity increase. When supply increases (curve shifts right), price decreases but quantity increases.',
        'controls': [
            {'key': '↑', 'action': 'Increase Demand'},
            {'key': '↓', 'action': 'Decrease Demand'},
            {'key': '→', 'action': 'Increase Supply'},
            {'key': '←', 'action': 'Decrease Supply'},
            {'key': 'R', 'action': 'Reset to Default'},
        ],
        'sketch_code': '''
let demandShift = 0;
let supplyShift = 0;
let equilibriumPrice = 0;
let equilibriumQty = 0;

function setup() {
    createCanvas(600, 400);
    textAlign(CENTER, CENTER);
    calculateEquilibrium();
}

function draw() {
    background(245);

    // Draw axes
    stroke(100);
    strokeWeight(2);
    line(50, 350, 550, 350); // X axis (Quantity)
    line(50, 50, 50, 350);   // Y axis (Price)

    // Labels
    fill(0);
    noStroke();
    textSize(14);
    text('Quantity', 300, 380);
    push();
    translate(20, 200);
    rotate(-HALF_PI);
    text('Price', 0, 0);
    pop();

    // Draw demand curve (downward sloping)
    stroke(200, 50, 50);
    strokeWeight(3);
    noFill();
    beginShape();
    for (let q = 0; q <= 500; q += 10) {
        let p = 300 - 0.5 * q + demandShift;
        let x = map(q, 0, 500, 50, 550);
        let y = map(p, 0, 300, 350, 50);
        vertex(x, y);
    }
    endShape();

    // Draw supply curve (upward sloping)
    stroke(50, 50, 200);
    strokeWeight(3);
    beginShape();
    for (let q = 0; q <= 500; q += 10) {
        let p = 50 + 0.4 * q + supplyShift;
        let x = map(q, 0, 500, 50, 550);
        let y = map(p, 0, 300, 350, 50);
        vertex(x, y);
    }
    endShape();

    // Draw equilibrium point
    fill(50, 150, 50);
    noStroke();
    let eqX = map(equilibriumQty, 0, 500, 50, 550);
    let eqY = map(equilibriumPrice, 0, 300, 350, 50);
    circle(eqX, eqY, 12);

    // Dotted lines to axes
    stroke(50, 150, 50);
    strokeWeight(1);
    drawingContext.setLineDash([5, 5]);
    line(eqX, eqY, eqX, 350);
    line(eqX, eqY, 50, eqY);
    drawingContext.setLineDash([]);

    // Legend
    textAlign(LEFT);
    textSize(14);
    fill(200, 50, 50);
    text('Demand', 70, 70);
    fill(50, 50, 200);
    text('Supply', 70, 95);
    fill(50, 150, 50);
    text('Equilibrium', 70, 120);

    // Display equilibrium values
    fill(0);
    textAlign(CENTER);
    textSize(16);
    text(`Equilibrium: P = $${equilibriumPrice.toFixed(0)}, Q = ${equilibriumQty.toFixed(0)} units`, 300, 30);
}

function calculateEquilibrium() {
    // Solve: 300 - 0.5q + demandShift = 50 + 0.4q + supplyShift
    // 250 + demandShift - supplyShift = 0.9q
    equilibriumQty = (250 + demandShift - supplyShift) / 0.9;
    equilibriumPrice = 300 - 0.5 * equilibriumQty + demandShift;
}

function keyPressed() {
    if (keyCode === UP_ARROW) {
        demandShift += 20;
        calculateEquilibrium();
    } else if (keyCode === DOWN_ARROW) {
        demandShift -= 20;
        calculateEquilibrium();
    } else if (keyCode === RIGHT_ARROW) {
        supplyShift -= 20;
        calculateEquilibrium();
    } else if (keyCode === LEFT_ARROW) {
        supplyShift += 20;
        calculateEquilibrium();
    } else if (key === 'r' || key === 'R') {
        demandShift = 0;
        supplyShift = 0;
        calculateEquilibrium();
    }
}
'''
    },

    'velocity': {
        'title': 'Velocity and Motion Simulator',
        'learning_objective': 'Understand velocity as a vector with magnitude and direction, and observe how it affects object motion.',
        'instructions': 'Watch the blue ball move with constant velocity. The red arrow shows the velocity vector. Use the controls to change the velocity direction and magnitude. Notice that velocity determines both speed (arrow length) and direction of motion.',
        'controls': [
            {'key': '↑', 'action': 'Increase upward velocity'},
            {'key': '↓', 'action': 'Increase downward velocity'},
            {'key': '→', 'action': 'Increase rightward velocity'},
            {'key': '←', 'action': 'Increase leftward velocity'},
            {'key': 'Space', 'action': 'Pause/Resume'},
            {'key': 'R', 'action': 'Reset position'},
        ],
        'sketch_code': '''
let position, velocity;
let paused = false;

function setup() {
    createCanvas(600, 400);
    position = createVector(300, 200);
    velocity = createVector(2, 1);
}

function draw() {
    background(240);

    // Update position if not paused
    if (!paused) {
        position.add(velocity);

        // Wrap around edges
        if (position.x > width) position.x = 0;
        if (position.x < 0) position.x = width;
        if (position.y > height) position.y = 0;
        if (position.y < 0) position.y = height;
    }

    // Draw grid for reference
    stroke(200);
    strokeWeight(1);
    for (let x = 0; x < width; x += 50) {
        line(x, 0, x, height);
    }
    for (let y = 0; y < height; y += 50) {
        line(0, y, width, y);
    }

    // Draw object
    fill(50, 100, 200);
    noStroke();
    circle(position.x, position.y, 30);

    // Draw velocity vector
    stroke(200, 50, 50);
    strokeWeight(3);
    let arrowEnd = p5.Vector.add(position, p5.Vector.mult(velocity, 20));
    line(position.x, position.y, arrowEnd.x, arrowEnd.y);

    // Arrow head
    push();
    translate(arrowEnd.x, arrowEnd.y);
    rotate(velocity.heading());
    fill(200, 50, 50);
    noStroke();
    triangle(-8, -4, -8, 4, 0, 0);
    pop();

    // Display velocity magnitude and components
    fill(0);
    noStroke();
    textAlign(LEFT);
    textSize(14);
    text(`Velocity: (${velocity.x.toFixed(1)}, ${velocity.y.toFixed(1)})`, 10, 20);
    text(`Speed: ${velocity.mag().toFixed(1)} units/frame`, 10, 40);
    text(paused ? 'PAUSED' : 'Running', 10, 60);
}

function keyPressed() {
    if (keyCode === UP_ARROW) {
        velocity.y -= 0.5;
    } else if (keyCode === DOWN_ARROW) {
        velocity.y += 0.5;
    } else if (keyCode === RIGHT_ARROW) {
        velocity.x += 0.5;
    } else if (keyCode === LEFT_ARROW) {
        velocity.x -= 0.5;
    } else if (key === ' ') {
        paused = !paused;
    } else if (key === 'r' || key === 'R') {
        position.set(300, 200);
    }
}
'''
    },

    'ecosystem': {
        'title': 'Predator-Prey Ecosystem Simulator',
        'learning_objective': 'Observe how predator and prey populations affect each other in a simple ecosystem model.',
        'instructions': 'Watch the green prey and red predator populations change over time. The graph shows population levels. Notice the cyclical pattern: when prey are abundant, predators increase. As predators increase, prey decrease. Then predators decrease due to lack of food, allowing prey to recover.',
        'controls': [
            {'key': '↑', 'action': 'Increase prey birth rate'},
            {'key': '↓', 'action': 'Decrease prey birth rate'},
            {'key': '→', 'action': 'Increase predator efficiency'},
            {'key': '←', 'action': 'Decrease predator efficiency'},
            {'key': 'Space', 'action': 'Pause/Resume'},
            {'key': 'R', 'action': 'Reset simulation'},
        ],
        'sketch_code': '''
let preyPop = 100;
let predatorPop = 20;
let preyBirthRate = 0.05;
let predationRate = 0.001;
let predatorDeathRate = 0.03;
let conversionRate = 0.0005;

let history = [];
let maxHistory = 200;
let paused = false;

function setup() {
    createCanvas(600, 400);
}

function draw() {
    background(245);

    // Update populations if not paused
    if (!paused && frameCount % 2 === 0) {
        let preyGrowth = preyBirthRate * preyPop;
        let predation = predationRate * preyPop * predatorPop;
        let predatorGrowth = conversionRate * preyPop * predatorPop;
        let predatorDeath = predatorDeathRate * predatorPop;

        preyPop += preyGrowth - predation;
        predatorPop += predatorGrowth - predatorDeath;

        // Prevent extinction or explosion
        preyPop = constrain(preyPop, 5, 500);
        predatorPop = constrain(predatorPop, 2, 200);

        history.push({prey: preyPop, predator: predatorPop});
        if (history.length > maxHistory) {
            history.shift();
        }
    }

    // Draw graph area
    fill(255);
    stroke(200);
    strokeWeight(1);
    rect(50, 50, 500, 250);

    // Draw axes
    stroke(100);
    line(50, 300, 550, 300); // X axis (time)
    line(50, 50, 50, 300);   // Y axis (population)

    // Labels
    fill(0);
    noStroke();
    textAlign(CENTER);
    textSize(12);
    text('Time →', 300, 330);
    push();
    translate(20, 175);
    rotate(-HALF_PI);
    text('Population', 0, 0);
    pop();

    // Draw population lines
    if (history.length > 1) {
        // Prey line (green)
        stroke(50, 200, 50);
        strokeWeight(2);
        noFill();
        beginShape();
        for (let i = 0; i < history.length; i++) {
            let x = map(i, 0, maxHistory, 50, 550);
            let y = map(history[i].prey, 0, 500, 300, 50);
            vertex(x, y);
        }
        endShape();

        // Predator line (red)
        stroke(200, 50, 50);
        beginShape();
        for (let i = 0; i < history.length; i++) {
            let x = map(i, 0, maxHistory, 50, 550);
            let y = map(history[i].predator, 0, 200, 300, 50);
            vertex(x, y);
        }
        endShape();
    }

    // Legend and current values
    textAlign(LEFT);
    fill(50, 200, 50);
    textSize(14);
    text(`Prey: ${preyPop.toFixed(0)}`, 70, 370);
    fill(200, 50, 50);
    text(`Predators: ${predatorPop.toFixed(0)}`, 200, 370);
    fill(0);
    text(paused ? 'PAUSED' : 'Running', 400, 370);
}

function keyPressed() {
    if (keyCode === UP_ARROW) {
        preyBirthRate = min(preyBirthRate + 0.01, 0.15);
    } else if (keyCode === DOWN_ARROW) {
        preyBirthRate = max(preyBirthRate - 0.01, 0.01);
    } else if (keyCode === RIGHT_ARROW) {
        predationRate = min(predationRate + 0.0002, 0.003);
    } else if (keyCode === LEFT_ARROW) {
        predationRate = max(predationRate - 0.0002, 0.0002);
    } else if (key === ' ') {
        paused = !paused;
    } else if (key === 'r' || key === 'R') {
        preyPop = 100;
        predatorPop = 20;
        history = [];
    }
}
'''
    }
}


def detect_simulation_type(competency: str) -> Optional[str]:
    """
    Detect if a simulation is appropriate and which type.

    Args:
        competency: The learning competency/objective

    Returns:
        Simulation type key or None if no match
    """
    competency_lower = competency.lower()

    # Economics simulations
    if any(keyword in competency_lower for keyword in [
        'supply and demand', 'supply & demand', 'market equilibrium',
        'equilibrium price', 'demand curve', 'supply curve'
    ]):
        return 'supply_demand'

    # Physics simulations
    if any(keyword in competency_lower for keyword in [
        'velocity', 'motion', 'speed and direction', 'vector'
    ]):
        return 'velocity'

    # Biology/ecology simulations
    if any(keyword in competency_lower for keyword in [
        'predator prey', 'predator-prey', 'ecosystem', 'population dynamics',
        'food chain', 'food web'
    ]):
        return 'ecosystem'

    return None


def should_generate_simulation(competency: str) -> bool:
    """
    Determine if simulation generation is appropriate.

    Args:
        competency: The learning competency/objective

    Returns:
        True if simulation should be generated
    """
    return detect_simulation_type(competency) is not None


def generate_simulation(competency: str, output_path: str) -> bool:
    """
    Generate HTML simulation file from competency.

    Args:
        competency: The learning competency/objective
        output_path: Path to save the HTML file

    Returns:
        True if simulation was generated, False if no match
    """
    sim_type = detect_simulation_type(competency)

    if sim_type is None:
        print(f"No simulation template matches competency.")
        print(f"Competency: {competency}")
        print(f"\nAvailable simulation types:")
        for key in SIMULATION_TEMPLATES.keys():
            print(f"  - {key}")
        return False

    # Get template data
    sim_data = SIMULATION_TEMPLATES[sim_type]

    # Load HTML template
    template_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'templates',
        'simulation_template.html'
    )

    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}", file=sys.stderr)
        return False

    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    template = Template(template_content)

    # Render template
    html_output = template.render(
        title=sim_data['title'],
        learning_objective=sim_data['learning_objective'],
        instructions=sim_data['instructions'],
        controls=sim_data['controls'],
        sketch_code=sim_data['sketch_code']
    )

    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"Generated {sim_type} simulation: {output_path}")
    return True


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python generate_simulation.py <competency> <output.html>")
        print()
        print("Example:")
        print('  python generate_simulation.py "Students will analyze supply and demand" simulation.html')
        sys.exit(1)

    competency = sys.argv[1]
    output_path = sys.argv[2]

    success = generate_simulation(competency, output_path)

    # Exit 0 regardless - "no simulation needed" is not an error
    sys.exit(0)


if __name__ == "__main__":
    main()
