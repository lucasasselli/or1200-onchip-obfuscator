`include "obf_defines.v"


module obf_lut_gen(
    addr,
    out_sub,
    out_imm,
);

parameter MEM_FILE = "lut0.list";

input [`OBF_LUT_ADDR_WIDTH-1:0] addr;
output [`OBF_LUT_OUT_WIDTH-1:0] out_sub;
output [`OBF_LUT_OUT_WIDTH-1:0] out_imm;

reg [`OBF_LUT_OUT_WIDTH-1:0] mem [0:255];

initial begin
    $readmemb(MEM_FILE, mem);
end

assign out_sub = mem[addr];
assign out_imm = mem[addr+1];

endmodule
