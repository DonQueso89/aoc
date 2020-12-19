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

function evaluate2(expr)
    termstack = []
    iresult = 1
    op = *
    for c in expr
        if c == '('
            push!(termstack, Term(iresult, op))
            push!(termstack, Term(0, +))
            iresult, op = 1, *
        elseif c == '*'
            push!(termstack, Term(iresult, *))
            iresult, op = 1, *
        elseif isdigit(c)
            iresult = op(iresult, parse(Int, c))
        elseif c == ' '
            continue
        elseif c == '+'
            op = +
        elseif c == ')'
            while termstack[end].n > 0
                lhs = pop!(termstack)
                iresult = lhs.op(iresult, lhs.n)
            end
            lhs = pop!(termstack)
            iresult = lhs.op(iresult, lhs.n)

            if length(termstack) > 0 && termstack[end].op == +
                lhs = pop!(termstack)
                iresult = lhs.op(iresult, lhs.n)
            end
        end
    end

    while length(termstack) > 0
        lhs = pop!(termstack)
        iresult = lhs.op(iresult, lhs.n)
    end

    return iresult
end

println("1: $(sum(map(evaluate, exprs)))")
println("2: $(sum(map(evaluate2, exprs)))")