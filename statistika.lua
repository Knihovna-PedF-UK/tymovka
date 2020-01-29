-- statistika rezervací týmovky v roce

-- pokud nezadáme rok, bude počítat všechny doby
local process_year = arg[1]
local zpracuj = false
local count = 0
for line in io.lines() do
  if line:match("timestamp") then
    zpracuj = true
  elseif zpracuj == true then
    -- najít timestamp
    local timestamp = tonumber(line:match("([0-9]+)"))
    local year = os.date("%Y", timestamp)
    -- spočítat buď jen zadaný rok, nebo celkově
    if process_year then 
      if process_year == year then
        count = count + 1  
      end
    else
      count = count + 1
    end
    zpracuj = false
  end
end
print(count)
