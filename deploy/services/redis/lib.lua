#!lua name=matchmaking
local function verify_pop(keys, args)
    local src = keys[1]
    local opp = keys[2]
    local elem = args[1]
    local len = redis.call('LLEN', src)
    if len ~= 0 then
        local exists = redis.call('LREM', opp, 0, elem)
        if exists ~= 0 then
            return redis.call('LPOP', src)
        end
    end
    return nil
end

redis.register_function('VPOP', verify_pop)