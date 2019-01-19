#!/usr/bin/env ruby

def setup(inp)
    numeric_rgx = /^\d+$/
    wires = Hash.new
    inp.each do |instruction|
        expression = instruction[0].split(" ")
        if expression.length > 1
            # Ensure that operator is always last
            expression[-1], expression[-2] = expression[-2], expression[-1]
        else
            if expression[0].match numeric_rgx
                expression = expression[0].to_i
            else
                expression = expression[0]
            end
        end
        wires[instruction[1]] = expression
    end
    return wires
end

def solve(wires)
    operators = {
        "OR" => lambda { |a, b| return a | b  },
        "AND" => lambda { |a, b| return a & b  },
        "RSHIFT" => lambda { |a, b| return a >> b },
        "LSHIFT" => lambda { |a, b| return a << b },
        "NOT" => lambda { |a| return ~a < 0 ? 2 ** 16 + ~a : ~a }
    }

    numeric_rgx = /^\d+$/
    solved = Hash.new
    while solved.length < wires.length do
        wires.each do |wire, gate|
            if gate == nil
                # noop
                0
            elsif gate.is_a? Integer
                # We can always solve this
                solved[wire] = gate
                wires[wire] = nil
            elsif gate.is_a? String
                # We solve this if the string is solvable
                if solved.has_key? gate
                    solved[wire] = solved[gate]
                    wires[wire] = nil
                end
            else
                # We can solve this if the non-numeric operands are solvable
                ops, operand = gate.slice(0, gate.length - 1), gate[-1]
                can_solve = ops.select { |op| op.match(numeric_rgx) == nil } .map { |op| solved.has_key? op } .all?
                if can_solve
                    # Replace all operators with their values
                    ops = ops.map { |op| op.match(numeric_rgx) != nil ? op.to_i : solved[op] }
                    solved[wire] = operators[operand].call(*ops)
                    wires[wire] = nil
                end
            end
        end
    end
    return solved
end

input = File.read(ARGV[0]).split("\n").map {|x| x.split(" -> ") }
solved = Hash.new

wires = setup(input)

solved = solve(wires)
puts "part 1: #{solved["a"]}"

wires = setup(input)
wires["b"] = solved["a"]
solved = solve(wires)
puts "part 2: #{solved["a"]}"
