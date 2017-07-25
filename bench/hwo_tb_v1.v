`include "../rtl/verilog/hwo_top.v" 

module hwo_tb_v1(
   // Empty 
);
reg clk;
reg rst;
reg [31:0] id_insn;
wire [31:0] io_insn;

reg [31:0] iram [0:88];

integer i;

initial begin
  $readmemh("insn.data", iram);
  clk = 0;
  rst = 0;
  i = 0;
  #5 rst = 1;
end

// Clk generator
always begin
    #5 clk = !clk;
end

always @(posedge clk) begin
    id_insn <= iram[i];
    i <= i + 1;
end

hwo_top dut(clk, reset, id_insn, io_insn);

endmodule
