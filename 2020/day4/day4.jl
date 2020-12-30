import Base.parse  #  explicit imports for method extension


if length(ARGS) > 0
    infile = ARGS[1]
else
    infile = "input4"
end

input = readlines(infile)


COLORS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

parse(s::SubString) = parse(Int16, "$s")
parse(s::String) = parse(Int16, "$s")

ops = Dict([
 ("byr", (bin=1, valid=x -> 1920 <= parse(x) <= 2002)),
 ("iyr" ,(bin=2, valid=x -> 2010 <= parse(x) <= 2020)),
 ("eyr" ,(bin=3, valid=x -> 2020 <= parse(x) <= 2030)),
 ("hgt" ,(bin=4, valid=x -> endswith(x, "cm") ? 150 <= parse(replace(x, r"cm" => "")) <= 193 : 59 <= parse(replace(x, r"in" => "")) <= 76)),
 ("hcl" ,(bin=5, valid=x -> match(r"^#[a-f0-9]{6}$", x) !== nothing)),
 ("ecl" ,(bin=6, valid=x -> x in COLORS)),
 ("pid" ,(bin=7, valid=x -> match(r"^[0-9]{9}$", x) !== nothing)),
 ("cid" ,(bin=8, valid=x -> true)),
])

 setbit(b:: Int16, n:: Int64) =  b | 1 << (n-1)

function solve()
    n_present = 0
    n_valid = 0
    present_collector::Int16 = 0b0
    valid_collector::Int16 = 0b0

    for line in input
        if isempty(line)
            n_present += present_collector in  (255, 127) ? 1 : 0
            n_valid += valid_collector in  (255, 127) ? 1 : 0
            present_collector = 0 
            valid_collector = 0 
        end

        for s in split(line)
            k, v = split(s, ":")
            present_collector = setbit(present_collector, ops[k].bin)                

            if ops[k].valid(v)
                valid_collector = setbit(valid_collector, ops[k].bin)
            end
        end
    end
    n_present += present_collector in  (255, 127) ? 1 : 0
    n_valid += valid_collector in  (255, 127) ? 1 : 0

    return n_present, n_valid
end

p, v = solve()
println("1: $p")
println("2: $v")
