// WARNING:
// This code was generated by a tool. DO NOT MODIFY!

`include "obf_defines.v"

module obf_pt2(
    index,
    addr,
);

input [`OBF_IGU_WIDTH-1:0] index;
output reg [`OBF_LUT_ADDR_WIDTH-1:0] addr;

always @(index) begin
    case(index)
		`OBF_IGU_WIDTH'd24: addr = `OBF_LUT_ADDR_WIDTH'd1;
		`OBF_IGU_WIDTH'd25: addr = `OBF_LUT_ADDR_WIDTH'd6;
		`OBF_IGU_WIDTH'd6: addr = `OBF_LUT_ADDR_WIDTH'd11;

        default: addr = `OBF_LUT_ADDR_WIDTH'd0;
    endcase
end
endmodule
