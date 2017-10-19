module obf_rndgen(
    clk, rst, 
    en, out
);

// TODO Make it more generic
output reg [7:0] out;
input clk, rst, en;

wire feedback;

assign feedback = (out[7] ^ out[5] ^ out[4] ^ out[3]);

always @(posedge clk, posedge rst)
begin
    if (rst)
        out <= 8'hF1;
    else if (en)
        out <= {out[6:0],feedback};
    else
        out <= out;
end
endmodule
