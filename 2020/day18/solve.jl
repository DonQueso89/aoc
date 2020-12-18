if length(ARGS) > 0
    fname = ARGS[1]
else
    fname = "input"
end

struct Term
    n::Int
    op::Function
end

exprs = readlines(open(fname))

function evaluate(expr)
    termstack = []
    iresult = 1
    op = *
    for c in expr
        if c == '('
            push!(termstack, Term(iresult, op))
            iresult, op = 1, *
        elseif isdigit(c)
            iresult = op(iresult, parse(Int, c))
        elseif c == ' '
            continue
        elseif c in ('*', '+')
            op = eval(Symbol(c))
        elseif c == ')'
            lhs = pop!(termstack)
            iresult = lhs.op(iresult, lhs.n)
        end
    end
    return iresult
end

println("1: $(sum(map(evaluate, exprs)))")